import logging
import threading
import time
import sys

import message
from .state import Leader, Candidate, Follower
from .storage import Storage
from .transport import Transport

"""
ActiveNodes take part in all votes, keep track of the consensus log, and immediately converts to a Candidate
on election timeout.
"""
NODE_MODE_ACTIVE = 1

"""
Passive mode take part in all votes, keep track of the consensus log, but never nominates itself for leadership.
"""
NODE_MODE_PASSIVE = 2

"""
ReluctantNodes take part in all votes, keep track of the consensus log, but only converts to a Candidate if it
receives only request requests from Candidates behind in the consensus log history.
"""
NODE_MODE_RELUCTANT = 3

_modeNames = {
    NODE_MODE_ACTIVE: 'active',
    NODE_MODE_RELUCTANT: 'reluctant',
    NODE_MODE_PASSIVE: 'passive',
    'active': NODE_MODE_ACTIVE,
    'reluctant': NODE_MODE_RELUCTANT,
    'passive': NODE_MODE_PASSIVE,
}

"""
Consensus network has a leader and there is a majority of nodes connected.
"""
NODE_STATUS_GREEN = 'green'

"""
Consensus network has a leader, there is a majority of nodes connected, but applied index is significantly behind
commit index.
"""
NODE_STATUS_YELLOW = 'yellow'

"""
Consensus network either does not have a leader or there is not a majority of nodes connected.
"""
NODE_STATUS_RED = 'red'


def get_mode_name(mode):
    return _modeNames.get(mode, 'Unknown mode %s' % mode)


class Node(object):
    def __init__(self, mode, name, neighbourhood, storage,
                 election_timeout=500, heartbeat_timeout=250, vote_timeout=150,
                 logger=None):
        """
        :param int mode: `NODE_MODE_ACTIVE`|`NODE_MODE_PASSIVE`|`NODE_MODE_RELUCTANT`
        :param str name: <hostname/ip_address>:<port>
        :param str[] neighbourhood: List of neighbours
        :param Storage storage: Storage for the Node's state
        :param int election_timeout: follower election timeout in milliseconds
        :param int heartbeat_timeout: leader heartbeat timeout in milliseconds
        :param int vote_timeout: candidate vote timeout in milliseconds
        :param logging.Logger logger:
        """
        self.mode = mode
        self.name = name
        self.neighbourhood = list(neighbourhood)
        self.neighbours = list(neighbourhood)
        self.storage = storage

        # Ensure neighbourhood includes this node
        self.neighbourhood.append(name)
        self.neighbourhood = list(set(self.neighbourhood))
        # Ensure neighbours excludes this node
        self.neighbours = list(set(self.neighbours))
        self.neighbours.remove(name)

        self.election_timeout = election_timeout / 1000.0
        self.heartbeat_timeout = heartbeat_timeout / 1000.0
        self.vote_timeout = vote_timeout / 1000.0

        self.logger = logger or logging.getLogger(__name__)

        self.lock = threading.Lock()
        self.leader = (None, None)
        self.transport = None
        self.request_address = None
        self.state = storage.retrieve(self)
        self.time_outs = dict.fromkeys(self.neighbours, time.time())
        self.last_heard = dict.fromkeys(self.neighbours)
        self.extend_timeout()

        self.leadership_required = False
        self.apply_thread = None
        self.transport_thread = None
        self.neighbour_threads = []
        self.active = False
        self.shutdown_flag = False

    def __del__(self):
        self.storage.persist(self.state)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.storage.persist(self.state)

    def handle_signal(self, signum, frame):
        self.shutdown()
        sys.exit(signum)

    def reset_state(self, new_data):
        self.state = Follower.from_state(self.state)
        self.state.set_current_state(new_data)

    def is_leader(self, neighbour=None):
        """
        If no `neighbour` is given this whether this `Node` is the leader
        otherwise if `neighbour` is the leader.
        :param str neighbour:
        :return: If this `Node` is the leader or if `neighbour` is the leader
        """
        if neighbour is None:
            return isinstance(self.state, Leader)
        else:
            return self.leader[0] == neighbour

    def has_leader(self):
        """
        :return: True if there currently is an elected Leader
        """
        return self.is_leader() or self.leader[0] is not None

    def get_leader(self):
        return self.name if self.is_leader() else self.leader[0]

    def get_request_address(self):
        """
        :return: The address and port that commands should be sent to
        """
        return self.request_address if self.is_leader() else self.leader[1]

    def has_majority(self, count):
        """
        :param int count:
        :return: True if `count` is a majority
        """
        return count > int((len(self.neighbourhood) - 1) / 2)

    def status(self):
        """
        :return: The status of the node
        """
        if self.transport is None or not self.has_leader():
            return NODE_STATUS_RED
        elif self.is_leader() and not self.has_majority(len(self.transport.connected()) + 1):
            return NODE_STATUS_RED
        elif (self.state.last_applied - self.state.commit_index) > 500:
            return NODE_STATUS_YELLOW
        else:
            return NODE_STATUS_GREEN

    def log(self, level, msg):
        self.logger.log(level, "[%s->%-9s(%2d)] %s" % (self.name, self.state, self.state.current_term, msg))

    def apply_entry(self, state):
        """
        Apply the next entry.
        :param state:
        """
        # increment the state's last applied
        state.last_applied += 1
        state.cluster_applied[self.name] = state.last_applied

        # persist changes
        self.storage.persist(state)

        self.log(logging.INFO, "Applied entry: %s" % state.last_applied)

        if self.is_leader():
            self.state.statistics.set_applied_timestamp(self.state.commit_index, time.time())

    def on_message(self, msg):
        """
        :param pyraftlog.message.Message msg:
        :rtype: pyraftlog.message.Message|pref
        """
        with self.lock:
            state = self.state
            response = None
            self.log(logging.DEBUG, "Message received: %s" % msg)
            self.last_heard[msg.sender] = time.time()

            # If request/response message term > our current term become a follower
            if msg.term > state.current_term:
                self.log(logging.INFO, "This Node is behind the current term of %s(%2d)" % (msg.sender, msg.term))
                state = Follower.from_state(state, msg.term)
                self.state = state

            # Perform an action based on the received message type and current state
            if msg.type == message.APPEND_ENTRIES:
                # Update when the sender last sent a message (if not a response)
                self.extend_timeout(msg.sender)

                # Note if the leadership has changed
                if self.leader[0] != msg.sender:
                    self.log(logging.WARN, "Accepted Leadership: %s" % msg.sender)

                self.leader = (msg.sender, msg.data['request_address'])
                state, response = state.on_append_entries(msg)

            elif msg.type == message.VOTE_REQUEST:
                state, response = state.on_vote_request(msg)

                # Leadership might be required if this candidate wasn't eligible
                self.leadership_required = state.current_term not in state.voted_for
                if self.mode == NODE_MODE_RELUCTANT and self.leadership_required:
                    self.log(logging.INFO, "Candidate was not eligible: %s" % msg.sender)
                    # Set the timeout for this Reluctant Node to become candidate to the shortest election timeout
                    self.time_outs = dict.fromkeys(self.neighbours, time.time() + self.election_timeout)

            elif msg.type == message.VOTE_RESPONSE:
                state, response = state.on_vote_response(msg)

            elif msg.type == message.APPEND_RESPONSE:
                state, response = state.on_append_response(msg)
                # Leadership is no longer required if an active node is up to date
                self.leadership_required = msg.mode != NODE_MODE_ACTIVE or \
                    state.log.index() != state.match_index[msg.sender]
                if self.mode == NODE_MODE_RELUCTANT and not self.leadership_required:
                    self.log(logging.INFO, "Message sender is eligible: %s" % msg.sender)
                    state = Follower.from_state(state, msg.term)

            # Entries are applied elsewhere

            # Update the current state
            self.state = state

            # Return the response
            if response and response.recipient in self.neighbours:
                self.log(logging.DEBUG, "Sending response : %s" % response)
                return response
            return None

    def has_timed_out(self, neighbour=None):
        """
        :param str neighbour:
        :return: True if `neighbour` has timed out
        """
        if neighbour is None:
            return max(self.time_outs.values()) <= time.time()
        else:
            return self.time_outs[neighbour] <= time.time()

    def reset_timeout(self, neighbour=None, timeout_time=None):
        """
        :param str neighbour:
        :param float timeout_time:
        """
        timeout_time = timeout_time or time.time()
        if neighbour is not None:
            self.log(logging.DEBUG, "Timeout reset for %s" % neighbour)
            self.time_outs[neighbour] = timeout_time
        else:
            self.log(logging.DEBUG, "Timeouts reset")
            self.time_outs = dict.fromkeys(self.neighbours, timeout_time)

    def extend_timeout(self, neighbour=None):
        """
        :param str neighbour:
        """
        if neighbour is not None:
            current = self.time_outs[neighbour]
            updated = self.state.next_timeout_time(self.time_outs[neighbour])
            self.log(logging.DEBUG, "Timeout extended for %s : %d" % (neighbour, updated-current))
            self.time_outs[neighbour] = updated

        else:
            self.log(logging.DEBUG, "Timeouts extended")
            timeout_time = self.state.next_timeout_time(max(self.time_outs.values()))
            self.time_outs = dict.fromkeys(self.neighbours, timeout_time)

    def activate(self, transport):
        """
        Start the threads to active this node.
        :param Transport transport:
        """
        self.log(logging.INFO, "Node starting")
        self.active = True
        self.shutdown_flag = False

        self.transport = transport
        self.extend_timeout()

        # Apply entries thread
        self.apply_thread = threading.Thread(target=self.thread_apply_entries)
        self.apply_thread.daemon = True
        self.apply_thread.start()

        # Publish/timeout thread
        for neighbour in self.neighbours:
            thread = threading.Thread(target=self.thread_neighbour_timeout, args=[transport, neighbour])
            thread.daemon = True
            thread.start()
            self.neighbour_threads.append(thread)

        # Subscribe thread
        self.transport_thread = threading.Thread(target=transport.subscribe, args=[self])
        self.transport_thread.daemon = True
        self.transport_thread.start()

    def deactivate(self):
        """
        Stop all threads gracefully and deactivate this node (Leaves API running)
        """
        self.log(logging.INFO, "Deactivating Node")
        # Set active flag to False
        self.active = False
        self.transport.shutdown()

        # Wait for threads to stop
        while self.apply_thread.is_alive():
            pass

        neighbours_stopped = False
        while not neighbours_stopped:
            neighbours_stopped = True
            for thread in self.neighbour_threads:
                if thread.is_alive():
                    neighbours_stopped = False

    def shutdown(self):
        """
        Stop all threads gracefully and shutdown this node
        """
        self.log(logging.INFO, "Node shutting down")
        self.deactivate()
        self.shutdown_flag = True

    def thread_apply_entries(self):
        """
        Start a while true loop to apply committed entries.
        """
        self.log(logging.DEBUG, "Starting to apply entries")
        while self.active:
            # If commit index > last applied and not set to auto apply
            if self.state.commit_index > self.state.last_applied:
                try:
                    self.apply_entry(self.state)
                except Exception as e:
                    self.log(logging.CRITICAL, "(%s) %s" % (type(e), e))

        self.log(logging.DEBUG, "Thread for applying entries has stopped")

    def thread_neighbour_timeout(self, transport, neighbour):
        """
        :param Transport transport:
        :param str neighbour:
        """
        self.log(logging.DEBUG, "Starting thread to work with %s" % neighbour)
        while self.active:
            try:
                if isinstance(self.state, Leader) and self.has_timed_out(neighbour):
                    self.on_timeout_leader(transport, neighbour)

                elif isinstance(self.state, Leader) and self.state.missing_entries(neighbour):
                    self.on_behind_entries(transport, neighbour)

                elif isinstance(self.state, Candidate) and self.has_timed_out(neighbour):
                    self.on_timeout_candidate(transport, neighbour)

                elif isinstance(self.state, Follower) and self.has_timed_out():
                    self.on_timeout_follower(transport, neighbour)

            except Exception as e:
                transport.handle_exception(neighbour, e)
                self.extend_timeout(neighbour)
        self.log(logging.DEBUG, "Thread for neighbour %s has stopped" % neighbour)

    def on_behind_entries(self, transport, neighbour):
        """
        :param Transport transport:
        :param str neighbour:
        """
        transport.publish(self, self.state.append_entry_message(neighbour))
        self.extend_timeout(neighbour)

    def on_timeout_leader(self, transport, neighbour):
        """
        :param Transport transport:
        :param str neighbour:
        """
        self.log(logging.DEBUG, "Firing heartbeat for %s" % neighbour)
        transport.publish(self, self.state.append_entry_message(neighbour, True))
        self.extend_timeout(neighbour)

    def on_timeout_candidate(self, transport, neighbour):
        """
        :param Transport transport:
        :param str neighbour:
        """
        # Increment current term
        if self.state.increment_term(neighbour):

            # Persist changes
            self.storage.persist(self.state)

            # Reset timeouts to send the initial vote request
            self.reset_timeout()

        self.log(logging.DEBUG, "Sending vote request to %s" % neighbour)
        # Send out vote request
        transport.publish(self, self.state.vote_request_message(neighbour))

        self.extend_timeout(neighbour)

    def on_timeout_follower(self, transport, neighbour):
        """
        :param Transport transport:
        :param str neighbour:
        """
        if self.mode == NODE_MODE_PASSIVE:
            return

        if self.mode == NODE_MODE_RELUCTANT and not self.leadership_required:
            self.log(logging.INFO, "Leadership might be required of this reluctant node")
            self.leadership_required = True
            self.extend_timeout(neighbour)
            return

        with self.lock:
            if not isinstance(self.state, Follower):
                return

            self.log(logging.WARN, "Converting to candidate (Leader: %s)" % self.get_leader())

            # Clear the current leader
            self.leader = (None, None)

            # Reset timeouts to send the initial vote request
            self.reset_timeout()

            # Convert to candidate
            self.state = Candidate.from_state(self.state)
