import unittest

from friends.data.friendslist.mock_repository import MockRepository
from friends.server import FriendsService
from proto.friends_pb2 import (GetFriendsForUserRequest,
                               DeleteConnectionBetweenUsersRequest,
                               CreateConnectionForUsersRequest)
from proto.common_pb2 import User


class TestFriendRelationships(unittest.TestCase):
    server = None

    @classmethod
    def setUpClass(cls):
        repo = MockRepository(
            {
                1: [5, 6, 8],
                5: [1, 2, 3, 6],
                8: [1, 3, 5],
                10: [20, 30, 40],
                20: [5, 10],
                25: [5, 10],
                30: [35],
                35: [30],
            }
        )
        cls.server = FriendsService(
            repo
        )

    """
    Check that if we attempt to get an existing user's friends we get the proper list
    """
    def test_get_existing_friends_list(self):
        resp = self.server.get_user_friends_from_cache(GetFriendsForUserRequest(
            user=User(
                userID=5,
                userName="test",
                email="test",
            )
        ))
        friends = list(resp.friends)
        self.assertListEqual(friends, [1, 2, 3, 6])

    """
    Check that if we attempt to get a not existing user's friends we get an empty proper list
    """
    def test_get_nonexisting_friends_list(self):
        resp = self.server.get_user_friends_from_cache(GetFriendsForUserRequest(
            user=User(
                userID=1000,
                userName="test",
                email="test",
            )
        ))
        friends = list(resp.friends)
        self.assertListEqual(friends, [])

    """
    Check that if we delete 
    """
    def test_delete_friend_existing(self):
        success = self.server.delete_friend_from_cache(
            DeleteConnectionBetweenUsersRequest(
                firstUserID=8,
                secondUserID=1,
            )
        )
        self.assertTrue(success)
        u1_friends_list = list(self.server.get_user_friends_from_cache(
            GetFriendsForUserRequest(
                user=User(
                    userID=8,
                )
            )
        ).friends)
        u2_friends_list = list(self.server.get_user_friends_from_cache(
            GetFriendsForUserRequest(
                user=User(
                    userID=1,
                )
            )
        ).friends)
        self.assertListEqual(u1_friends_list, [3, 5])
        self.assertListEqual(u2_friends_list, [5, 6])

    def test_delete_friend_not_existing(self):
        success = self.server.delete_friend_from_cache(
            DeleteConnectionBetweenUsersRequest(
                firstUserID=1000,
                secondUserID=1,
            )
        )
        self.assertFalse(success)

    def test_add_friend_existing(self):
        success = self.server.add_friend_to_cache(
            CreateConnectionForUsersRequest(
                firstUserID=20,
                secondUserID=25,
            )
        )
        self.assertTrue(success.success)
        u1_friends_list = list(self.server.get_user_friends_from_cache(
            GetFriendsForUserRequest(
                user=User(
                    userID=20,
                )
            )
        ).friends)
        u2_friends_list = list(self.server.get_user_friends_from_cache(
            GetFriendsForUserRequest(
                user=User(
                    userID=25,
                )
            )
        ).friends)
        self.assertListEqual(u1_friends_list, [5, 10, 25])
        self.assertListEqual(u2_friends_list, [5, 10, 20])

    def test_add_friend_already_existing(self):
        success = self.server.add_friend_to_cache(
            CreateConnectionForUsersRequest(
                firstUserID=30,
                secondUserID=35,
            )
        )
        self.assertFalse(success.success)
