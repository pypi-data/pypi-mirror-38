import pytest
import pyraftlog

from pyraftlog.nodes import Node
from pyraftlog.states import Follower
from pyraftlog.states import Candidate
from pyraftlog.states import Leader
from pyraftlog.storage import Storage
from pyraftlog.messages import Message


# Leader behaviour tests
def test_leader_on_leader_timeout():
    node = Node(pyraftlog.NODE_MODE_PASSIVE, "node1", ["node1", "node2", "node3"], Storage())
    leader = Leader(node)

    assert leader.current_term == 0
    assert node.message_board.len("node2") == 0
    assert node.message_board.len("node3") == 0
    leader.on_leader_timeout()
    assert leader.current_term == 0
    assert node.message_board.len("node2") == 1
    assert node.message_board.len("node3") == 1
    assert node.message_board.get("node2").type == Message.APPEND_ENTRIES
    assert node.message_board.get("node3").type == Message.APPEND_ENTRIES
