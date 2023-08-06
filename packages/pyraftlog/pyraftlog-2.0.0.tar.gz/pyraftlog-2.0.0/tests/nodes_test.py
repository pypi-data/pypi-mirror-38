import pytest
import pyraftlog

from pyraftlog.node import Node
from pyraftlog.state import Follower
from pyraftlog.state import Candidate
from pyraftlog.state import Leader
from pyraftlog.storage import Storage


def test_node_is_leader():
    node = Node(pyraftlog.NODE_MODE_PASSIVE, "node1", ["node1", "node2", "node3"], Storage())

    assert not node.is_leader()
    node.state = Candidate.from_state(node.state)
    assert not node.is_leader()
    node.state = Leader.from_state(node.state)
    assert node.is_leader()


def test_get_leader():
    node = Node(pyraftlog.NODE_MODE_PASSIVE, "node1", ["node1", "node2", "node3"], Storage())

    leader = Leader(Node(pyraftlog.NODE_MODE_PASSIVE, "node2", ["node1", "node2", "node3"], Storage()))

    assert node.get_leader() is None
    node.on_message(leader.append_entry_message("node1", True))
    assert node.get_leader() == leader.node.name
    node.state = Leader.from_state(node.state)
    assert node.get_leader() == node.name


def test_get_request_address():
    node = Node(pyraftlog.NODE_MODE_PASSIVE, "node1", ["node1", "node2", "node3"], Storage())

    leader = Leader(Node(pyraftlog.NODE_MODE_PASSIVE, "node2", ["node1", "node2", "node3"], Storage()))

    assert node.get_request_address() == node.request_address
    node.on_message(leader.append_entry_message("node1", True))
    assert node.get_request_address() == leader.node.request_address


def test_has_majority():
    node = Node(pyraftlog.NODE_MODE_PASSIVE, "node1", ["node1", "node2", "node3"], Storage())

    assert not node.has_majority(0)
    assert not node.has_majority(1)
    assert node.has_majority(2)
    assert node.has_majority(3)

    node = Node(pyraftlog.NODE_MODE_PASSIVE, "node1", ["node1", "node2", "node3", "node4", "node5"], Storage())

    assert not node.has_majority(0)
    assert not node.has_majority(1)
    assert not node.has_majority(2)
    assert node.has_majority(3)
    assert node.has_majority(4)
    assert node.has_majority(5)


def test_on_message_leader_behind_message_term():
    node = Node(pyraftlog.NODE_MODE_PASSIVE, "node1", ["node1", "node2", "node3"], Storage())
    node.state = Leader.from_state(node.state)

    follower = Follower(Node(pyraftlog.NODE_MODE_PASSIVE, "node2", ["node1", "node2", "node3"], Storage()))
    follower.current_term = 2

    node.on_message(follower.append_response_message("node1", False))
    assert type(node.state) == Follower
    assert node.state.current_term == follower.current_term


def test_on_message_candidate_behind_message_term():
    node = Node(pyraftlog.NODE_MODE_PASSIVE, "node1", ["node1", "node2", "node3"], Storage())
    node.state = Candidate.from_state(node.state)

    follower = Follower(Node(pyraftlog.NODE_MODE_PASSIVE, "node2", ["node1", "node2", "node3"], Storage()))
    follower.current_term = 2

    node.on_message(follower.vote_response_message("node1", False))
    assert type(node.state) == Follower
    assert node.state.current_term == follower.current_term


def test_on_message_follower_behind_message_term():
    node = Node(pyraftlog.NODE_MODE_PASSIVE, "node1", ["node1", "node2", "node3"], Storage())

    follower = Follower(Node(pyraftlog.NODE_MODE_PASSIVE, "node2", ["node1", "node2", "node3"], Storage()))
    follower.current_term = 2

    node.on_message(follower.append_response_message("node1", False))
    assert type(node.state) == Follower
    assert node.state.current_term == follower.current_term




