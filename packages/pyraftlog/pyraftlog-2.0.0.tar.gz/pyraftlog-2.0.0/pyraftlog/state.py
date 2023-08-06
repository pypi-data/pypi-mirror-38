import logging
import random
import time

import message
from .log import Log
from .statistics import Statistics

APPEND_MAX = 100


class State(object):
    def __init__(self, node=None):
        """
        :param Node node:
        """
        self.node = node
        # Persistent state on all nodes
        # latest term server has seen (increases monotonically)
        self.current_term = 1
        # candidate id that received vote in current term
        self.voted_for = {}
        # log entries; each entry contains command for state machine, and term when entry was received by leader
        self.log = Log()

        # Volatile state on all nodes
        # index of highest log entry known to be committed (increases monotonically)
        self.commit_index = 0
        # index of highest log entry applied to state machine (increases monotonically)
        self.last_applied = 0

        # Added values for log reduction
        self.cluster_applied = {node.name: 0} if node else None
        self.log_reduction = False

        # Volatile state on leaders
        # for each node, index of the index log entry to send to that node
        self.next_index = {}
        # for each node, index of highest log entry known to be replicated on node (increases monotonically)
        self.match_index = {}
        for neighbour in node.neighbours if node else []:
            self.next_index[neighbour] = self.log.next_index(self.log.index())
            self.match_index[neighbour] = 0

        # Volatile state on candidates
        self.votes = {}

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

    def __getstate__(self):
        return {
            "current_term": self.current_term,
            "voted_for": self.voted_for,
            "log": self.log,

            "commit_index": self.commit_index,
            "last_applied": self.last_applied,

            "cluster_applied": self.cluster_applied,
            "log_reduction": self.log_reduction,
        }

    def __str__(self):
        return self.__class__.__name__

    def get_current_state(self, index):
        if index == 0:
            log = self.log.tail()
        else:
            if self.log.contains(index):
                log = self.log.get(index)
            else:
                return None

        return {
            'last_term': log[0],
            'last_index': log[1],
            'last_value': log[2]
        }

    def set_current_state(self, data):
        # -1 as append increments cindex before appending log
        self.log.cindex = data['last_index'] - 1
        self.log.append(data['last_term'], data['last_value'])
        self.commit_index = self.log.index()
        self.last_applied = self.log.index()

        for neighbour in self.node.neighbours if self.node else []:
            self.next_index[neighbour] = self.log.next_index(self.log.index())
            self.match_index[neighbour] = 0

    @classmethod
    def from_state(cls, from_state, message_term=None):
        """
        Create a state based on `from_state`.
        :param State from_state:
        :param int message_term:
        :rtype: State
        """
        state = cls(from_state.node)
        state.populate(from_state)
        if message_term:
            state.current_term = message_term

        return state

    def populate(self, from_state):
        self.current_term = from_state.current_term
        self.voted_for = from_state.voted_for
        self.log = from_state.log

        self.commit_index = from_state.commit_index
        self.last_applied = from_state.last_applied

        self.cluster_applied = from_state.cluster_applied
        self.log_reduction = from_state.log_reduction

    def next_timeout_time(self, prev_timeout_time):
        """ Generate a new timeout. """
        raise NotImplementedError()

    def increment_term(self, neighbour):
        """
        Increment the current term of the state if the neighbour has voted in this term.
        :param str neighbour:
        """
        if neighbour in self.votes or self.voted_for[self.current_term] != self.node.name:
            self.current_term += 1
            self.node.log(logging.DEBUG, "Neighbour %s has already voted this term so increasing to %d" % (
                neighbour,
                self.current_term
            ))

            self.voted_for = {self.current_term: self.node.name}
            self.votes = {self.node.name: True}
            return True

    def missing_entries(self, neighbour):
        """
        :param str neighbour:
        """
        return False

    def on_vote_request(self, msg):
        """
        This is called when there is a vote request.
        :param message.Message msg: The vote requested message
        :rtype: State, message.Message
        """
        self.node.log(logging.INFO, "Vote request received from %s" % msg.sender)

        data = msg.data
        # If the candidate's term is behind ours
        if msg.term < self.current_term:
            return self, self.vote_response_message(data['candidate_id'], False)

        # If we haven't voted this term or we voted for this candidate and
        if self.current_term not in self.voted_for or self.voted_for[self.current_term] == data['candidate_id']:
            # If candidate's log is at least as up-to-date as ours
            if self.log.index() <= data['last_log_index']:
                self.node.log(logging.INFO, "Casting vote for %s" % msg.sender)
                self.voted_for = {self.current_term: data['candidate_id']}
                # persist changes
                self.node.storage.persist(self)
                return self, self.vote_response_message(data['candidate_id'], True)

        return self, self.vote_response_message(data['candidate_id'], False)

    def on_vote_response(self, msg):
        return self, None

    def on_append_entries(self, msg):
        """
        This is called when there is a request to append an entry to the log.
        :param message.Message msg: The append entries message
        :rtype: State, message.Message
        """
        state = self
        data = msg.data

        # If we are not a Follower
        if not isinstance(state, Follower):
            state = Follower.from_state(state)

        # Reply false if the message term < our current term
        if msg.term < state.current_term:
            state.node.log(logging.INFO, "This Node is ahead of the messenger's term (%2d < %2d)" % (
                msg.term,
                state.current_term
            ))
            return state, state.append_response_message(msg.sender, False)

        # fail fast if prev log index has been reduced
        if state.log.tail().index > data['prev_log_index']:
            return state, state.append_response_message(msg.sender, False)

        # can't be up to date if our log is smaller than prev log index
        if state.log.index() < data['prev_log_index']:
            state.node.log(logging.INFO, "This Node is behind the log index (%2d < %2d)" % (state.log.index(),
                                                                                            data['prev_log_index']))
            return state, state.append_response_message(msg.sender, False)

        # If our term doesn't match the leaders
        if state.log.get(data['prev_log_index']).term != data['prev_log_term']:
            entry = state.log.get(data['prev_log_index'])
            state.node.log(logging.WARN, "This Node has inconsistent logs (%2d,%2d) != (%2d,%2d)" % (
                entry.term,
                entry.index,
                data['prev_log_term'],
                data['prev_log_index']
            ))
            if state.log.tail().index <= data['prev_log_index']:
                state.log.rewind(data['prev_log_index'] - 1)
            return state, state.append_response_message(msg.sender, False)

        # The induction proof held so we append any new entries
        for index, e in enumerate(data['entries'], data['prev_log_index'] + 1):
            state.node.log(logging.INFO, "Considering entry: (%2d,%2d)" % (e[0], e[1]))
            # If an existing entry conflicts with a new one trust the leaders log
            if state.log.index() >= index and state.log.get(index).term != e[0]:
                entry = state.log.get(index)
                state.node.log(logging.WARN, "This Node has inconsistent logs (%2d,%2d) != (%2d,%2d)" % (
                    entry.term,
                    entry.index,
                    e[0],
                    e[1]
                ))
                if state.log.tail().index <= data['prev_log_index']:
                    state.log.rewind(index - 1)

            # Append any new entries not already in the log
            if state.log.index() < index:
                state.node.log(logging.WARN, "Appending entry to log at index %2d" % e[1])
                state.log.append(e[0], e[2])

        # Update our commit index
        if data['leader_commit'] > state.commit_index:
            state.commit_index = min(data['leader_commit'], state.log.index())

        # Update our cluster_applied and log reduction
            state.cluster_applied = data['cluster_applied']
            state.log_reduction = data['log_reduction']
        # Reduce the log
        if state.log_reduction:
            if state.log.reduce(min(state.cluster_applied.values())):
                state.node.log(logging.DEBUG, "Reduced log to %2d" % len(state.log))

        # persist changes
        state.node.storage.persist(state)

        return state, state.append_response_message(msg.sender, True)

    def on_append_response(self, msg):
        return self, None

    def append_log_entry(self, command):
        return False

    def vote_request_message(self, recipient):
        return message.Message.build(message.VOTE_REQUEST, self, recipient, {
            "candidate_id": self.node.name,
            "last_log_index": self.log.index(),
            "last_log_term": self.log.head().term if self.log else 0,
        })

    def vote_response_message(self, candidate, response):
        return message.Message.build(message.VOTE_RESPONSE, self, candidate, {
            "response": response
        })

    def append_entry_message(self, recipient, heartbeat=False):
        next_log_index = self.next_index[recipient]
        prev_log_index = self.log.prev_index(next_log_index)
        entries = [] if heartbeat else self.log.slice(next_log_index, APPEND_MAX)

        return message.Message.build(message.APPEND_ENTRIES, self, recipient, {
            "leader_id": self.node.name,
            "prev_log_index": prev_log_index,
            "prev_log_term": self.log.get(prev_log_index).term,
            "entries": entries,
            "leader_commit": self.commit_index,

            # Inform followers of request address for clients
            "request_address": self.node.request_address,

            # Inform followers of whether log reduction is active
            # and where the whole cluster is up to
            "log_reduction": self.log_reduction,
            "cluster_applied": self.cluster_applied,
        })

    def append_response_message(self, recipient, response):
        return message.Message.build(message.APPEND_RESPONSE, self, recipient, {
            "response": response,
            "last_applied": self.last_applied,

            # Inform the leader the head of our log
            "last_appended": self.log.index(),
        })


class Leader(State):
    def populate(self, from_state):
        super(Leader, self).populate(from_state)

        for neighbour in self.node.neighbours:
            self.next_index[neighbour] = self.log.next_index(self.log.index())

        self.statistics = Statistics()

    def next_timeout_time(self, prev_timeout_time):
        if prev_timeout_time > time.time():
            return prev_timeout_time

        timeout = self.node.heartbeat_timeout
        multiplier = 1 + int((time.time() - prev_timeout_time) / timeout)
        return min(time.time() + timeout, prev_timeout_time + (multiplier * timeout))

    def on_append_response(self, msg):
        response = None
        data = msg.data
        if not data['response']:
            # Attempt to catch up the node that is behind
            if self.next_index[msg.sender] > 0:
                self.next_index[msg.sender] = self.log.prev_index(self.next_index[msg.sender])
                response = self.append_entry_message(msg.sender)
        else:
            # Update the match next indexes for the message sender
            self.match_index[msg.sender] = min(self.log.index(), self.next_index[msg.sender])
            self.next_index[msg.sender] = min(self.log.index() + 1, self.log.next_index(data['last_appended']))

            # Respond with next entry if still behind
            if self.next_index[msg.sender] <= self.log.index():
                response = self.append_entry_message(msg.sender)

            # Update commit index if there is a majority
            for index in sorted(self.match_index.values(), reverse=True):
                if index > self.commit_index:
                    count = sum(1 for x in self.match_index.values() if x >= index)
                    if self.node.has_majority(count + 1):
                        self.node.log(logging.WARN, "Committed log to index (%2d)" % index)
                        self.commit_index = index
                        self.statistics.set_committed_timestamp(self.commit_index, time.time())
                        # persist changes
                        self.node.storage.persist(self)

            # Update `cluster_applied`
            self.cluster_applied[msg.sender] = data['last_applied']

        # Perform log reduction
        if self.log_reduction:
            if self.log.reduce(min(self.cluster_applied.values())):
                self.node.log(logging.DEBUG, "Reduced log to %2d" % len(self.log))
                # persist changes
                self.node.storage.persist(self)

        if response:
            self.node.log(logging.DEBUG, "Response message: %s" % response)

        return self, response

    def append_log_entry(self, command):
        index = self.log.append(self.current_term, command)
        self.node.log(logging.DEBUG, "Appended log entry at index %2d" % self.log.index())
        self.statistics.set_append_timestamp(index, time.time())

        # persist changes
        self.node.storage.persist(self)

        return index

    def missing_entries(self, neighbour):
        """
        :param str neighbour:
        :return: True if the neighbour is missing entries or if the match index is behind our commit index
        """
        return self.next_index[neighbour] <= self.log.index() or self.match_index[neighbour] < self.commit_index


class Candidate(State):
    def next_timeout_time(self, prev_timeout_time):
        if prev_timeout_time > time.time():
            return prev_timeout_time

        timeout = self.node.vote_timeout
        multiplier = 1 + int((time.time() - prev_timeout_time) / timeout)
        return min(time.time() + timeout, prev_timeout_time + (multiplier * timeout))

    def on_vote_response(self, msg):
        # Ignore messages from previous terms
        if msg.term < self.current_term:
            self.node.log(logging.ERROR, "Ignoring %s" % msg)
            return self, None

        self.node.log(logging.DEBUG, "Received vote from %s: %r" % (msg.sender, msg.data['response']))
        # Update the votes tally
        self.votes[msg.sender] = msg.data['response']

        # If we have successfully received a majority
        if self.node.has_majority(self.votes.values().count(True)):
            # Promote yourself to leader
            self.node.log(logging.WARN, "Converting to Leader (Log index: %s)" % self.log)
            state = Leader.from_state(self)
            self.node.reset_timeout()

            return state, None

        else:
            if self.votes.values().count(True) == 1 and self.votes.values().count(False) >= 1:
                return Follower.from_state(self), None

            return self, None

    @classmethod
    def from_state(cls, from_state, message_term=None):
        state = super(Candidate, cls).from_state(from_state, message_term)
        state.current_term += 1
        state.voted_for = {state.current_term: state.node.name}
        state.votes[state.node.name] = True
        return state


class Follower(State):
    def next_timeout_time(self, prev_timeout_time):
        return time.time() + random.uniform(self.node.election_timeout, 2 * self.node.election_timeout)
