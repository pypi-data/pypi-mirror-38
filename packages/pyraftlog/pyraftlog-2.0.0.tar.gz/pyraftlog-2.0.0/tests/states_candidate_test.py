import pytest
import pyraftlog

from pyraftlog.nodes import Node
from pyraftlog.states import Follower
from pyraftlog.states import Candidate
from pyraftlog.states import Leader
from pyraftlog.storage import Storage
from pyraftlog.messages import Message


# Candidate behaviour tests
def test_candidate_on_leader_timeout():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    candidate = Candidate(node)

    assert candidate.current_term == 0
    assert node.message_board.len("node2") == 0
    assert node.message_board.len("node3") == 0
    candidate.on_leader_timeout()
    assert candidate.current_term == 1
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.VOTE_REQUEST
    assert node.message_board.get("node3").type == Message.VOTE_REQUEST


def test_candidate_on_leader_timeout_after_vote_failure():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    candidate = Candidate(node)
    assert candidate.current_term == 0
    candidate.on_leader_timeout()
    assert candidate.current_term == 1
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.VOTE_REQUEST
    assert node.message_board.get("node3").type == Message.VOTE_REQUEST

    failure = Message(Message.VOTE_RESPONSE, "node2", "node1", 1, {"response": False})

    state, _ = candidate.on_vote_response(failure)
    assert type(state) == Candidate
    assert candidate.current_term == 1
    assert node.message_board.len("node2") == 0
    assert node.message_board.len("node3") == 0

    candidate.on_leader_timeout()
    assert candidate.current_term == 2
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.VOTE_REQUEST
    assert node.message_board.get("node3").type == Message.VOTE_REQUEST


def test_candidate_on_leader_timeout_after_vote_no_response():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    candidate = Candidate(node)
    assert candidate.current_term == 0
    candidate.on_leader_timeout()
    assert candidate.current_term == 1
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.VOTE_REQUEST
    assert node.message_board.get("node3").type == Message.VOTE_REQUEST

    candidate.on_leader_timeout()
    assert candidate.current_term == 1
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.VOTE_REQUEST
    assert node.message_board.get("node3").type == Message.VOTE_REQUEST


def test_candidate_on_vote_response_success_node2():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    candidate = Candidate(node)
    candidate.on_leader_timeout()
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.VOTE_REQUEST
    assert node.message_board.get("node3").type == Message.VOTE_REQUEST

    success = Message(Message.VOTE_RESPONSE, "node2", "node1", 1, {"response": True})

    state, _ = candidate.on_vote_response(success)
    assert type(state) == Leader
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.APPEND_ENTRIES
    assert node.message_board.get("node3").type == Message.APPEND_ENTRIES


def test_candidate_on_vote_response_success_node3():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    candidate = Candidate(node)
    candidate.on_leader_timeout()
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.VOTE_REQUEST
    assert node.message_board.get("node3").type == Message.VOTE_REQUEST

    success = Message(Message.VOTE_RESPONSE, "node3", "node1", 1, {"response": True})

    state, _ = candidate.on_vote_response(success)
    assert type(state) == Leader
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.APPEND_ENTRIES
    assert node.message_board.get("node3").type == Message.APPEND_ENTRIES


def test_candidate_on_vote_response_failure_node2():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    candidate = Candidate(node)
    candidate.on_leader_timeout()
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.VOTE_REQUEST
    assert node.message_board.get("node3").type == Message.VOTE_REQUEST

    failure = Message(Message.VOTE_RESPONSE, "node2", "node1", 1, {"response": False})

    state, _ = candidate.on_vote_response(failure)
    assert type(state) == Candidate
    assert node.message_board.len("node2") == 0
    assert node.message_board.len("node3") == 0


def test_candidate_on_vote_response_failure_node3():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    candidate = Candidate(node)
    candidate.on_leader_timeout()
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.VOTE_REQUEST
    assert node.message_board.get("node3").type == Message.VOTE_REQUEST

    failure = Message(Message.VOTE_RESPONSE, "node3", "node1", 1, {"response": False})

    state, _ = candidate.on_vote_response(failure)
    assert type(state) == Candidate
    assert node.message_board.len("node2") == 0
    assert node.message_board.len("node3") == 0


def test_candidate_on_append_entries():
    node = Node(pyraftlog.NODE_MODE_PASSIVE,"node1", ["node1", "node2", "node3"], Storage())
    candidate = Candidate(node)
    candidate.on_leader_timeout()

    leader = Leader(Node(pyraftlog.NODE_MODE_PASSIVE,"node2", ["node1", "node2", "node3"], Storage()))

    state, _ = candidate.on_append_entries(leader.append_entry_message("node1", True))
    assert type(state) == Follower
