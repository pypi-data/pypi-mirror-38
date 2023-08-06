import cPickle
import os
import tempfile

import redis

from .state import Follower


class Storage(object):
    def retrieve(self, node):
        """
        Retrieve the state of the given name from storage.
        Must always be a `Follower` as we have that is the default.
        :param pyraftlog.nodes.Node node:
        :return: The loaded state
        :rtype: Follower
        """
        return Follower(node)

    def persist(self, state):
        """
        Persist the given state to storage.
        :param State state:
        :return: True if successful
        :rtype: bool
        """
        return True


class FileStorage(Storage):
    def __init__(self, file_path):
        """
        :param str file_path: Path to the storage file
        """
        self.file_path = file_path

    def retrieve(self, node):
        state = Follower(node)
        if os.path.isfile(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'r') as f:
                state.populate(cPickle.loads(f.read()))

        return state

    def persist(self, state):
        # Atomically write the state to file
        with tempfile.NamedTemporaryFile(dir=os.path.dirname(self.file_path), delete=False) as t:
            t.write(cPickle.dumps(state, 2))
            t.flush()
            # os.fsync(t.fileno())
            os.rename(t.name, self.file_path)


class RedisStorage(Storage):
    def __init__(self, redis_client, key_prefix='raft_state_'):
        """
        :param redis.Redis redis_client:
        :param str key_prefix:
        """
        self.redis_client = redis_client
        self.key_prefix = key_prefix

    def retrieve(self, node):
        # Retrieve the data from redis
        state = Follower(node)
        value = self.redis_client.get(self.key_prefix + node.name)
        if value:
            value = cPickle.loads(value)
            state.populate(value)
            node.logger.info("Retrieved state (%2d,%2d)[%2d]" % (value['current_term'], value['commit_index'],
                                                                 len(state.log)))
        return state

    def persist(self, state):
        self.redis_client.set(self.key_prefix + state.node.name, cPickle.dumps(state, 2))
