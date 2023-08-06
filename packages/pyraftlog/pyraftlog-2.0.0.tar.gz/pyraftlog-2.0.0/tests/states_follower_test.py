import pytest
import pyraftlog

from pyraftlog.logs import Entry
from pyraftlog.nodes import Node
from pyraftlog.states import Follower
from pyraftlog.states import Candidate
from pyraftlog.states import Leader
from pyraftlog.storage import Storage
from pyraftlog.messages import Message


# Follower behaviour tests
def test_follower_on_leader_timeout():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)
    assert type(follower.on_leader_timeout()) == Candidate


def test_follower_on_append_entries_heartbeat():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)

    leader = Leader(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))

    state, _ = follower.on_append_entries(leader.append_entry_message("node1", True))
    assert type(state) == Follower
    assert state == follower


def test_follower_on_vote_request_not_voted():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)

    candidate = Candidate(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))

    state, response = follower.on_vote_request(candidate.vote_request_message("node1"))
    assert type(state) == Follower
    assert state == follower
    assert response.type == Message.VOTE_RESPONSE
    assert response.data == {"response": True}


def test_follower_on_vote_request_already_voted():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)

    candidate2 = Candidate(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))
    candidate3 = Candidate(Node(pyraftlog.NODE_MODE_PASSIVE,"node3", ["node1", "node2", "node3"], Storage()))

    follower.on_vote_request(candidate2.vote_request_message("node1"))
    state, response = follower.on_vote_request(candidate3.vote_request_message("node1"))
    assert type(state) == Follower
    assert state == follower
    assert response.type == Message.VOTE_RESPONSE
    assert response.data == {"response": False}


def test_follower_on_vote_request_with_elected_leader():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower1 = Follower(node)

    candidate2 = Candidate(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))
    candidate3 = Candidate(Node(pyraftlog.NODE_MODE_PASSIVE,"node3", ["node1", "node2", "node3"], Storage()))

    # node2 becomes leader after a successful vote
    candidate2.on_leader_timeout()
    _, response = follower1.on_vote_request(candidate2.node.message_board.get("node1"))
    candidate3.on_vote_request(candidate2.node.message_board.get("node3"))
    leader2, _ = candidate2.on_vote_response(response)
    follower1.on_append_entries(leader2.node.message_board.get("node1"))
    follower3, _ = candidate3.on_append_entries(leader2.node.message_board.get("node3"))

    follower1.current_term = leader2.current_term
    follower3.current_term = leader2.current_term

    # node3 times out and starts a new election
    candidate3 = follower3.on_leader_timeout()
    state, response = follower1.on_vote_request(candidate3.node.message_board.get("node1"))
    assert type(state) == Follower
    assert state == follower1
    assert response.type == Message.VOTE_RESPONSE
    assert response.data == {"response": True}


def test_follower_on_vote_request_with_candidate_behind_current_term():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)

    candidate2 = Candidate(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))
    candidate3 = Candidate(Node(pyraftlog.NODE_MODE_PASSIVE,"node3", ["node1", "node2", "node3"], Storage()))

    # node2 becomes leader after a successful vote
    candidate2.on_leader_timeout()
    _, response = follower.on_vote_request(candidate2.node.message_board.get("node1"))
    leader2, _ = candidate2.on_vote_response(response)
    follower.on_append_entries(leader2.node.message_board.get("node1"))

    state, response = follower.on_vote_request(candidate3.vote_request_message("node1"))
    assert type(state) == Follower
    assert state == follower
    assert response.type == Message.VOTE_RESPONSE
    assert response.data == {"response": False}


def test_follower_on_vote_request_with_candidate_behind_index():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)

    candidate = Candidate(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))

    follower.current_term = 1
    candidate.current_term = 1
    follower.log.append(1, None)
    follower.log.append(1, None)

    state, response = follower.on_vote_request(candidate.vote_request_message("node1"))
    assert type(state) == Follower
    assert state == follower
    assert response.type == Message.VOTE_RESPONSE
    assert response.data == {"response": False}


def test_follower_on_append_entries_message_term_behind():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)

    leader = Leader(Node(pyraftlog.NODE_MODE_PASSIVE, "node2", ["node1", "node2", "node3"], Storage()))

    follower.current_term = 2
    leader.current_term = 1

    state, response = follower.on_append_entries(leader.append_entry_message("node1", True))
    assert type(state) == Follower
    assert state == follower
    assert response.type == Message.APPEND_RESPONSE
    assert response.data == {"response": False, "last_applied": 0, "last_appended": 0}


def test_follower_on_append_entries_leader_index_ahead():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)

    leader = Leader(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))

    leader.append_log_entry(None)
    leader.next_index["node1"] = 2

    state, response = follower.on_append_entries(leader.append_entry_message("node1", True))
    assert type(state) == Follower
    assert state == follower
    assert response.type == Message.APPEND_RESPONSE
    assert response.data == {"response": False, "last_applied": 0, "last_appended": 0}


def test_follower_on_append_entries_leader_log_history_term_mismatch():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)

    leader = Leader(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))

    leader.current_term = 2
    follower.current_term = 2

    leader.log.append(2, None)
    follower.log.append(1, None)

    leader.next_index["node1"] = 1

    state, response = follower.on_append_entries(leader.append_entry_message("node1"))
    assert type(state) == Follower
    assert state == follower
    assert response.type == Message.APPEND_RESPONSE
    assert response.data == {"response": False, "last_applied": 0, "last_appended": 1}


def test_follower_on_append_entries_leader_log_entry_mismatch():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    follower = Follower(node)

    leader = Leader(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))

    leader.current_term = 2
    follower.current_term = 2

    leader.log.append(1, None)
    leader.log.append(2, None)
    follower.log.append(1, None)
    follower.log.append(1, None)

    leader.next_index["node1"] = 2

    message = leader.append_entry_message("node1")
    state, response = follower.on_append_entries(message)
    assert type(state) == Follower
    assert state == follower
    assert response.type == Message.APPEND_RESPONSE
    assert response.data['response']
    assert follower.log.head() == Entry(2, 2, None)
