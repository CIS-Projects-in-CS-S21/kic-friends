import unittest
import random

from friends.data.friendsgraph.friend_finding.friend_finder import FriendFinder
from friends.data.friendsgraph.mock_repository import MockGraph


class TestFriendFinder(unittest.TestCase):
    finder = None

    @classmethod
    def setUpClass(cls) -> None:

        graph = MockGraph()

        # I drew this and did Dijkstra's by hand
        graph.create_connection(0, 1)
        graph.create_connection(0, 2)
        graph.update_connection(0, 2, 1.5)
        graph.create_connection(0, 3)
        graph.update_connection(0, 3, 0.5)

        graph.create_connection(1, 2)
        graph.update_connection(1, 2, 0.4)

        graph.create_connection(2, 4)
        graph.create_connection(2, 3)
        graph.update_connection(2, 3, 0.8)

        graph.create_connection(3, 4)
        graph.update_connection(3, 4, 1.5)

        graph.create_connection(4, 5)
        graph.update_connection(4, 5, 0.2)
        graph.create_connection(4, 6)
        graph.update_connection(4, 6, 0.3)

        cls.finder = FriendFinder(
            graph
        )

    def testDijkstraCorrectness(self):
        d = self.finder.dijkstra(0)
        self.assertEqual(d[0], 0)
        self.assertEqual(d[1], 1.0)
        self.assertEqual(d[2], 1.3)
        self.assertEqual(d[3], 0.5)
        self.assertEqual(d[4], 2)
        self.assertEqual(d[5], 2.2)
        self.assertEqual(d[6], 2.3)

    def testGetRecommendations(self):
        d = self.finder.get_recommendations(2, 0)
        self.assertListEqual(d, [4, 5])

