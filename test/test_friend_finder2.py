import unittest
import logging

from friends.data.friendsgraph.friend_finding.friend_finder import FriendFinder
from friends.data.friendsgraph.mock_repository import MockGraph

logger = logging.getLogger('test')
FORMAT = "[%(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


class TestFriendFinder(unittest.TestCase):
    finder = None

    @classmethod
    def setUpClass(cls) -> None:
        graph = MockGraph()

        # Example from online for testing purposes
        graph.create_connection(0, 1)  # a to b
        graph.update_connection(0, 1, 3)  # weight 3
        graph.create_connection(0, 2)  # a to c
        graph.update_connection(0, 2, 5)  # weight 5
        graph.create_connection(0, 3)  # a to d
        graph.update_connection(0, 3, 6)  # weight 6

        graph.create_connection(1, 3)  # b to d
        graph.update_connection(1, 3, 2)  # weight 2

        graph.create_connection(2, 3)  # c to d
        graph.update_connection(2, 3, 2)  # weight 2
        graph.create_connection(2, 4)  # c to e
        graph.update_connection(2, 4, 6)  # weight 6
        graph.create_connection(2, 5)  # c to f
        graph.update_connection(2, 5, 3)  # weight 3
        graph.create_connection(2, 6)  # c to g
        graph.update_connection(2, 6, 7)  # weight 7

        graph.create_connection(3, 5)  # d to f
        graph.update_connection(3, 5, 7)  # weight 9

        graph.create_connection(4, 5)  # e to f
        graph.update_connection(4, 5, 5)  # weight 5
        graph.create_connection(4, 6)  # e to g
        graph.update_connection(4, 6, 2)  # weight 7

        graph.create_connection(5, 6)  # f to g
        graph.update_connection(5, 6, 1)  # weight 1

        cls.finder = FriendFinder(
            graph
        )

    def testDijkstraCorrectness2(self):
        d = self.finder.dijkstra(0)  # dijstra for a
        self.assertEqual(d[0], 0)  # a = 0
        self.assertEqual(d[1], 3)  # b = 3
        self.assertEqual(d[2], 5)  # c = 5
        self.assertEqual(d[3], 5)  # d = 5
        self.assertEqual(d[4], 11)  # e = 11
        self.assertEqual(d[5], 8)  # f = 8
        self.assertEqual(d[6], 9)  # g = 9
        logger.debug("Success")

    def testGetRecommendations2(self):
        d = self.finder.get_recommendations(2, 0)  # get top 2 recommendations
        self.assertListEqual(d, [5, 6])  # should be f, g
        logger.debug("Success")
