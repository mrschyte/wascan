import unittest
import queue

from util.misc import identity

class SetQueue(queue.Queue):
    def _init(self, maxsize):
        self.maxsize = maxsize
        self.queue = set()

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop()

class UniqueQueue(queue.Queue):
    def _init(self, maxsize):
        self.maxsize = maxsize
        self.history = set()
        self.queue = set()
        self.norm = identity

    def _put(self, item):
        item = self.norm(item)

        if item not in self.history:
            self.history.add(item)
            self.queue.add(item)

    def _get(self):
        return self.queue.pop()

class SelfTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
