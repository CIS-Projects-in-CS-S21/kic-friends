import unittest
import random
import logging

from friends.data.friendsgraph.friend_finding.priority_queue import HeapQueue

logger = logging.getLogger('test')
FORMAT = "[%(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


class TestPriorityQueue(unittest.TestCase):

    def test_heap_property(self):
        q = HeapQueue()
        for i in range(150):
            r = random.randint(0, 100)
            q.insert(i, r)
        prev_weight, _ = q.remove_top()
        while q.size() > 0:
            weight, value = q.remove_top()
            self.assertLessEqual(prev_weight, weight)
            prev_weight = weight
        logger.debug("Success")

    def test_decrease_value_heap_property(self):
        q = HeapQueue()
        for i in range(150):
            r = random.randint(1, 100)
            q.insert(i, r)
        q.decrease_weight(50, 0)
        prev_weight, value = q.remove_top()
        self.assertEqual(value, 50)
        while q.size() > 0:
            weight, value = q.remove_top()
            self.assertLessEqual(prev_weight, weight)
            prev_weight = weight
        logger.debug("Success")