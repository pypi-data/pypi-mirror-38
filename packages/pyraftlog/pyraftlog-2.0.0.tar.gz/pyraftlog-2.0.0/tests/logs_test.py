import pytest

from pyraftlog.log import Entry
from pyraftlog.log import Log


def test_log_get():
    log = Log()
    assert log.get(0) == Entry(0, 0, None)
    assert log.get(1) == Entry(0, 0, None)

    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert log.get(0) == Entry(0, 0, None)
    assert log.get(12) == Entry(0, 0, None)
    assert log.get(16) == Entry(0, 0, None)

    assert log.get(13) == Entry(11, 13, None)
    assert log.get(14) == Entry(11, 14, None)
    assert log.get(15) == Entry(11, 15, None)


def test_log_slice_empty():
    log = Log()
    assert log.slice(0) == []
    assert log.slice(1) == []


def test_log_slice_no_upper_bound():
    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert log.slice(0) == [Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)]
    assert log.slice(13) == [Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)]
    assert log.slice(14) == [Entry(11, 14, None), Entry(11, 15, None)]
    assert log.slice(15) == [Entry(11, 15, None)]


def test_log_slice_with_upper_bound():
    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert log.slice(0, 0) == []
    assert log.slice(0, 1) == [Entry(11, 13, None)]
    assert log.slice(0, 2) == [Entry(11, 13, None), Entry(11, 14, None)]
    assert log.slice(0, 3) == [Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)]
    assert log.slice(13, 0) == []
    assert log.slice(13, 1) == [Entry(11, 13, None)]
    assert log.slice(13, 2) == [Entry(11, 13, None), Entry(11, 14, None)]
    assert log.slice(13, 3) == [Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)]
    assert log.slice(14, 1) == [Entry(11, 14, None)]
    assert log.slice(14, 2) == [Entry(11, 14, None), Entry(11, 15, None)]
    assert log.slice(15, 1) == [Entry(11, 15, None)]


def test_log_index_empty():
    log = Log()
    assert log.index() == 0


def test_log_index_with_single_entry():
    log = Log([Entry(11, 13, None)])
    assert log.index() == 13


def test_log_index_with_multiple_entries():
    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert log.index() == 15


def test_log_head_empty():
    log = Log()
    assert log.head() == (0, 0, None)


def test_log_head_with_single_entry():
    log = Log([Entry(11, 13, None)])
    assert log.head() == (11, 13, None)


def test_log_head_with_multiple_entries():
    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert log.head() == (11, 15, None)


def test_log_tail_empty():
    log = Log()
    assert log.tail() == (0, 0, None)


def test_log_tail_with_single_entry():
    log = Log([Entry(11, 13, None)])
    assert log.tail() == (11, 13, None)


def test_log_tail_with_multiple_entries():
    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert log.tail() == (11, 13, None)


def test_log_prev_index_empty():
    log = Log()
    assert log.prev_index(1) == 0


def test_log_prev_index_with_single_entry():
    log = Log([Entry(11, 13, None)])
    assert log.prev_index(13) == 0
    assert log.prev_index(12) == 0


def test_log_prev_index_with_multiple_entries():
    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert log.cindex == 15
    assert log.prev_index(15) == 14
    assert log.prev_index(14) == 13
    assert log.prev_index(13) == 0
    assert log.prev_index(12) == 0
    assert log.prev_index(16) == 15
    assert log.prev_index(17) == 15


def test_log_next_index_empty():
    log = Log()
    assert log.next_index() == 1
    assert log.next_index(0) == 1
    assert log.next_index(1) == 1


def test_log_next_index_with_single_entry():
    log = Log([Entry(11, 13, None)])
    assert log.next_index() == 14
    assert log.next_index(13) == 14
    assert log.next_index(12) == 13
    assert log.next_index(0) == 13


def test_log_next_index_with_multiple_entries():
    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert log.next_index() == 16
    assert log.next_index(15) == 16
    assert log.next_index(14) == 15
    assert log.next_index(13) == 14
    assert log.next_index(12) == 13
    assert log.next_index(0) == 13
    assert log.next_index(16) == 16


def test_log_values():
    log = Log()
    assert log.values(0, 1) == []

    log = Log([Entry(11, 13, None)])
    assert log.values(0, 1) == []
    assert log.values(0, 13) == [{"term": 11, "index": 13, "value": None}]
    assert log.values(12, 13) == [{"term": 11, "index": 13, "value": None}]
    assert log.values(13, 13) == [{"term": 11, "index": 13, "value": None}]

    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert log.values(0, 1) == []
    assert log.values(0, 13) == [{"term": 11, "index": 13, "value": None}]
    assert log.values(12, 13) == [{"term": 11, "index": 13, "value": None}]
    assert log.values(13, 13) == [{"term": 11, "index": 13, "value": None}]
    assert log.values(13, 14) == [{"term": 11, "index": 13, "value": None}, {"term": 11, "index": 14, "value": None}]
    assert log.values(13, 15) == [
        {"term": 11, "index": 13, "value": None},
        {"term": 11, "index": 14, "value": None},
        {"term": 11, "index": 15, "value": None}
    ]
    assert log.values(14, 15) == [{"term": 11, "index": 14, "value": None}, {"term": 11, "index": 15, "value": None}]


def test_log_append():
    log = Log()
    assert len(log) == 0

    # log.append(Entry(11, 13, None))
    assert 1 == log.append(11, None)
    assert len(log) == 1
    # log.append(Entry(11, 14, None))
    assert 2 == log.append(11, None)
    assert len(log) == 2
    # log.append(Entry(11, 15, None))
    assert 3 == log.append(11, None)
    assert len(log) == 3


def test_log_reduce():
    log = Log()
    assert len(log) == 0
    assert not log.reduce(0)

    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert len(log) == 3
    assert not log.reduce(12)
    assert not log.reduce(13)
    assert log.reduce(14)
    assert len(log) == 2
    assert log.tail().index == 14
    assert not log.reduce(14)
    assert log.reduce(15)
    assert len(log) == 1
    assert log.tail().index == 15
    assert not log.reduce(15)
    assert log.reduce(16)
    assert len(log) == 0


def test_log_rewind():
    log = Log()
    assert len(log) == 0
    assert not log.rewind(0)

    log = Log([Entry(11, 13, None), Entry(11, 14, None), Entry(11, 15, None)])
    assert len(log) == 3
    assert not log.rewind(16)
    assert not log.rewind(15)
    assert log.rewind(14)
    assert len(log) == 2
    assert log.index() == 14
    assert not log.rewind(14)
    assert log.rewind(13)
    assert len(log) == 1
    assert log.index() == 13
    assert not log.rewind(13)
    assert log.rewind(12)
    assert len(log) == 0

