import threading
from collections import namedtuple


Entry = namedtuple("Entry", "term index value")
empty = Entry(0, 0, None)


class Log(object):
    def __init__(self, iterable=()):
        """
        :param iterable iterable:
        """
        self.entries = list(iterable)
        self.lock = threading.Lock()
        self.cindex = self.entries[-1].index if self.entries else 0
        self.offset = self.entries[0].index - 1 if self.entries else 0

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']
        return state

    def __len__(self):
        return len(self.entries)

    def __str__(self):
        return "%d,%d" % (self.head().term, self.head().index)

    def index(self):
        """
        :return: Latest index in the log
        """
        return self.cindex

    def get(self, idx):
        """
        :param int idx:
        :rtype: NamedTuple(Entry, term, index, value)
        """
        return self.entries[idx - (1 + self.offset)] if self.contains(idx) else empty

    def slice(self, idx, size=None):
        """
        :param int idx: from index
        :param int size: number of elements to include (up to)
        :return:
        """
        i = max(0, idx - (1 + self.offset))
        if size is None:
            return self.entries[i:]
        else:
            j = min(self.cindex, i) + size
            return self.entries[i:j]

    def contains(self, idx):
        """
        :param int idx:
        :rtype: Entry|tuple
        """
        return self.offset < idx <= self.cindex

    def head(self):
        """
        :rtype: NamedTuple(Entry, term, index, value)
        """
        return self.entries[-1] if self.entries else empty

    def tail(self):
        """
        :rtype: NamedTuple(Entry, term, index, value)
        """
        return self.entries[0] if self.entries else empty

    def prev_index(self, index):
        if self.cindex < index:
            return self.cindex
        if self.contains(index - 1):
            return index - 1
        else:
            return 0

    def next_index(self, index=None):
        if index is None:
            return self.cindex + 1

        if self.contains(index):
            return index + 1
        elif index > self.cindex:
            return self.cindex + 1
        else:
            return self.offset + 1

    def values(self, i, j):
        """
        :param int i:
        :param int j:
        :return: List of all log values from `i` to `j`
        :rtype: list
        """
        i = max(self.offset, i - 1) - self.offset
        j = min(self.cindex, j) - self.offset
        return [{"term": e.term, "index": e.index, "value": e.value} for e in self.entries[i:j]]

    def append(self, term, value):
        """
        :param int term:
        :param Any value:
        """
        with self.lock:
            self.cindex += 1
            self.entries.append(Entry(term, self.cindex, value))
            return self.cindex

    def reduce(self, index):
        """
        Remove all entries in the log with an index less than `index`.
        :param int index:
        :return: True if log effected
        :rtype: bool
        """
        with self.lock:
            current_size = len(self.entries)

            if index > self.cindex:
                self.entries = []
                self.offset = index
                self.cindex = index
            else:
                index = max(0, (min(index, self.cindex) - 1) - self.offset)
                self.entries = self.entries[index:]
                self.offset = self.entries[0].index - 1 if self.entries else 0

            return current_size != len(self.entries)

    def rewind(self, index):
        """
        Remove all entries in the log with an index greater than `index`.
        :param int index:
        :return: True if log effected
        :rtype: bool
        """
        with self.lock:
            current_size = len(self.entries)

            if index <= self.offset:
                self.entries = []
                self.offset = index
                self.cindex = index
            else:
                index = max(index + 1, self.offset)
                self.entries = self.entries[:index - (1 + self.offset)]
                self.cindex = self.entries[-1].index if self.entries else 0

            return current_size != len(self.entries)
