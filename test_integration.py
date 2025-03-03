import asyncio
import unittest
import os
import sys

from grpclib import GRPCError
from grpclib.client import Channel

# generated by protoc
from proto.common_pb2 import User
from proto.users_pb2 import GetUserByUsernameRequest, GetJWTTokenRequest
from proto.users_grpc import UsersStub
from proto.friends_pb2 import *
from proto.friends_grpc import FriendsStub


async def asyncSetUp(tests):
    location = 'localhost'
    if os.getenv("URL"):
        location = os.getenv("URL")
    channel = Channel(location, 50051)
    friends = FriendsStub(channel)
    tests.client = friends
    repo = {
        1: [5, 6, 8],
        5: [1, 2, 3, 6, 8, 20, 25],
        8: [1, 3, 5],
        10: [20, 40],
        20: [5, 10],
        25: [5, 10],
        30: [35],
        35: [30],
        102: [],
        103: [],
    }
    for uid in repo:
        for f_uid in repo[uid]:
            await tests.client.CreateConnectionForUsers(
                CreateConnectionForUsersRequest(
                    firstUserID=uid,
                    secondUserID=f_uid,
                )
            )
    await tests.client.AddAwaitingFriend(
        AddAwaitingFriendRequest(
            firstUserID=65,
            secondUserID=70,
        )
    )

    location = 'test.api.keeping-it-casual.com'

    channel = Channel(location, 50051)

    users_client = UsersStub(channel)

    try:
        res = await users_client.GetJWTToken(
            GetJWTTokenRequest(
                username="testuser",
                password="testpass",
            )
        )
    except GRPCError as error:
        print(f"error: {error}")
        print("Please run the integration test setup script prior to running these tests.")
        sys.exit(1)

    tests.token = res.token

    res = await users_client.GetUserByUsername(
        GetUserByUsernameRequest(
            username="testuser"
        ),
        metadata={"authorization": f"Bearer {tests.token}"}
    )

    tests.test_user_id = res.user.userID

    for friend in ["testuser1", "testuser2", "testuser3"]:
        res = await users_client.GetUserByUsername(
            GetUserByUsernameRequest(
                username=friend
            ),
            metadata={"authorization": f"Bearer {tests.token}"}
        )
        if friend == "testuser3":
            await tests.client.AddAwaitingFriend(
                AddAwaitingFriendRequest(
                    firstUserID=res.user.userID,
                    secondUserID=tests.test_user_id,
                )
            )
        else:
            await tests.client.CreateConnectionForUsers(
                CreateConnectionForUsersRequest(
                    firstUserID=tests.test_user_id,
                    secondUserID=res.user.userID,
                )
            )

    # this sets up a graph that was predrawn and checked with a manual run of the algorithm
    await tests.client.CreateConnectionForUsers(
        CreateConnectionForUsersRequest(
            firstUserID=1000,
            secondUserID=1001,
        )
    )
    await tests.client.CreateConnectionForUsers(
        CreateConnectionForUsersRequest(
            firstUserID=1000,
            secondUserID=1002,
        )
    )
    await tests.client.CreateConnectionForUsers(
        CreateConnectionForUsersRequest(
            firstUserID=1000,
            secondUserID=1003,
        )
    )
    await tests.client.CreateConnectionForUsers(
        CreateConnectionForUsersRequest(
            firstUserID=1001,
            secondUserID=1002,
        )
    )
    await tests.client.CreateConnectionForUsers(
        CreateConnectionForUsersRequest(
            firstUserID=1002,
            secondUserID=1004,
        )
    )
    await tests.client.CreateConnectionForUsers(
        CreateConnectionForUsersRequest(
            firstUserID=1002,
            secondUserID=1003,
        )
    )
    await tests.client.CreateConnectionForUsers(
        CreateConnectionForUsersRequest(
            firstUserID=1003,
            secondUserID=1004,
        )
    )
    await tests.client.CreateConnectionForUsers(
        CreateConnectionForUsersRequest(
            firstUserID=1004,
            secondUserID=1005,
        )
    )
    await tests.client.CreateConnectionForUsers(
        CreateConnectionForUsersRequest(
            firstUserID=1004,
            secondUserID=1006,
        )
    )

    await tests.client.UpdateConnectionBetweenUsers(
        UpdateConnectionBetweenUsersRequest(
            firstUserID=1000,
            secondUserID=1002,
            updateValue=1.5
        )
    )
    await tests.client.UpdateConnectionBetweenUsers(
        UpdateConnectionBetweenUsersRequest(
            firstUserID=1000,
            secondUserID=1003,
            updateValue=0.5
        )
    )
    await tests.client.UpdateConnectionBetweenUsers(
        UpdateConnectionBetweenUsersRequest(
            firstUserID=1001,
            secondUserID=1002,
            updateValue=0.4
        )
    )
    await tests.client.UpdateConnectionBetweenUsers(
        UpdateConnectionBetweenUsersRequest(
            firstUserID=1002,
            secondUserID=1003,
            updateValue=0.8
        )
    )
    await tests.client.UpdateConnectionBetweenUsers(
        UpdateConnectionBetweenUsersRequest(
            firstUserID=1003,
            secondUserID=1004,
            updateValue=1.5
        )
    )
    await tests.client.UpdateConnectionBetweenUsers(
        UpdateConnectionBetweenUsersRequest(
            firstUserID=1004,
            secondUserID=1005,
            updateValue=0.2
        )
    )
    await tests.client.UpdateConnectionBetweenUsers(
        UpdateConnectionBetweenUsersRequest(
            firstUserID=1004,
            secondUserID=1006,
            updateValue=0.3
        )
    )


class IntegrationTests(unittest.IsolatedAsyncioTestCase):
    client: FriendsStub = None
    token = None
    test_user_id = None

    # Check that if we attempt to get an existing user's friends we get the proper list
    async def test_get_existing_friends_list(self):
        resp = await self.client.GetFriendsForUser(GetFriendsForUserRequest(
            user=User(
                userID=5,
                userName="test",
                email="test",
            )
        ))
        friends = list(resp.friends)
        # includes friends who add
        self.assertListEqual(friends, [1, 2, 3, 6, 8, 20, 25])

    # Check that if we attempt to get a not existing user's friends we get an empty proper list
    async def test_get_nonexisting_friends_list(self):
        resp = await self.client.GetFriendsForUser(GetFriendsForUserRequest(
            user=User(
                userID=900,
                userName="test",
                email="test",
            )
        ))
        friends = list(resp.friends)
        self.assertListEqual(friends, [])

    # Check that if we delete an existing friend and user combo that we succeed
    async def test_delete_friend_existing(self):
        await self.client.DeleteConnectionBetweenUsers(
            DeleteConnectionBetweenUsersRequest(
                firstUserID=8,
                secondUserID=1,
            )
        )
        res1 = await self.client.GetFriendsForUser(
            GetFriendsForUserRequest(
                user=User(
                    userID=8,
                )
            )
        )
        u1_friends_list = sorted(list(res1.friends))

        res2 = await self.client.GetFriendsForUser(
            GetFriendsForUserRequest(
                user=User(
                    userID=1,
                )
            )
        )
        u2_friends_list = sorted(list(res2.friends))

        self.assertListEqual(u1_friends_list, [3, 5])
        self.assertListEqual(u2_friends_list, [5, 6])

    async def test_delete_friend_not_existing(self):
        with self.assertRaises(GRPCError) as context:
            await self.client.DeleteConnectionBetweenUsers(
                DeleteConnectionBetweenUsersRequest(
                    firstUserID=1000,
                    secondUserID=1,
                )
            )

        self.assertTrue(context.exception is not None)

    async def test_add_friend_existing(self):
        success = await self.client.CreateConnectionForUsers(
            CreateConnectionForUsersRequest(
                firstUserID=20,
                secondUserID=25,
            )
        )
        self.assertTrue(success.success)
        res1 = await self.client.GetFriendsForUser(
            GetFriendsForUserRequest(
                user=User(
                    userID=20,
                )
            )
        )
        u1_friends_list = sorted(list(res1.friends))
        res2 = await self.client.GetFriendsForUser(
            GetFriendsForUserRequest(
                user=User(
                    userID=25,
                )
            )
        )
        u2_friends_list = sorted(list(res2.friends))
        self.assertListEqual(u1_friends_list, [5, 10, 25])
        self.assertListEqual(u2_friends_list, [5, 10, 20])

    async def test_add_friend_already_existing(self):
        success = await self.client.CreateConnectionForUsers(
            CreateConnectionForUsersRequest(
                firstUserID=30,
                secondUserID=35,
            )
        )
        self.assertFalse(success.success)

    async def test_get_awaiting_friend(self):
        res = await self.client.GetAwaitingFriendsForUser(GetFriendsForUserRequest(
            user=User(
                userID=70,
            )
        )
        )
        self.assertListEqual(list(res.friends), [65])

    async def test_add_awaiting_friend(self):
        success = await self.client.AddAwaitingFriend(
            AddAwaitingFriendRequest(
                firstUserID=90,
                secondUserID=95,
            )
        )
        self.assertTrue(success.success)
        res2 = await self.client.GetAwaitingFriendsForUser(
            GetFriendsForUserRequest(
                user=User(
                    userID=95,
                )
            )
        )
        u2_friends_list = list(res2.friends)
        self.assertListEqual(u2_friends_list, [90])

    async def test_get_friends_usernames(self):
        res = await self.client.GetFriendsUsernamesForUser(
            GetFriendsForUserRequest(
                user=User(
                    userID=self.test_user_id,
                )
            ),
            metadata={"authorization": f"Bearer {self.token}"}
        )

        friends = sorted(list(res.friends))
        self.assertListEqual(friends, ["testuser1", "testuser2"])

    async def test_get_awaiting_friends_usernames(self):
        res = await self.client.GetAwaitingFriendsUsernamesForUser(
            GetFriendsForUserRequest(
                user=User(
                    userID=self.test_user_id,
                )
            ),
            metadata={"authorization": f"Bearer {self.token}"}
        )

        friends = sorted(list(res.friends))
        self.assertListEqual(friends, ["testuser3"])

    async def test_get_connection_between_existing_friends(self):
        res = await self.client.GetConnectionBetweenUsers(
            GetConnectionBetweenUsersRequest(
                firstUserID=30,
                secondUserID=35,
            )
        )
        self.assertEqual(res.connectionStrength, 1.0)

    async def test_get_connection_between_not_existing_friends(self):
        with self.assertRaises(GRPCError) as context:
            await self.client.GetConnectionBetweenUsers(
                GetConnectionBetweenUsersRequest(
                    firstUserID=102,
                    secondUserID=103,
                )
            )

        self.assertTrue(context.exception is not None)

    async def test_update_connection_between_existing_friends(self):
        res = await self.client.UpdateConnectionBetweenUsers(
            UpdateConnectionBetweenUsersRequest(
                firstUserID=20,
                secondUserID=25,
                updateValue=0.5
            )
        )
        self.assertEqual(res.connectionStrength, 0.5)
        res = await self.client.GetConnectionBetweenUsers(
            GetConnectionBetweenUsersRequest(
                firstUserID=20,
                secondUserID=25,
            )
        )
        self.assertEqual(res.connectionStrength, 0.5)

    async def test_update_connection_between_not_existing_friends(self):
        with self.assertRaises(GRPCError) as context:
            await self.client.GetConnectionBetweenUsers(
                GetConnectionBetweenUsersRequest(
                    firstUserID=102,
                    secondUserID=103,
                )
            )
        self.assertTrue(context.exception is not None)

    # TODO: This was tested prior to integrating the user service to get recommendations usernames,
    # we will need to adjust and create a friend graph of test users
    async def test_get_recommendations_for_user(self):
        res = await self.client.GetRecommendationsForUser(
            GetRecommendationsForUserRequest(
                user=User(
                    userID=1000,
                ),
                numberRecommendations=2
            ),
            metadata={"authorization": f"Bearer {self.token}"}
        )
        recommendations_list = res.recommendations
        self.assertEqual(len(recommendations_list), 2)
        self.assertEqual(recommendations_list[0].userID, 1004)
        self.assertEqual(recommendations_list[1].userID, 1005)


async def main():
    t = IntegrationTests()
    await asyncSetUp(t)
    await t.test_get_friends_usernames()
    await t.test_get_awaiting_friends_usernames()
    await t.test_get_existing_friends_list()
    await t.test_get_nonexisting_friends_list()
    await t.test_delete_friend_existing()
    await t.test_delete_friend_not_existing()
    await t.test_add_friend_existing()
    await t.test_add_friend_already_existing()
    await t.test_add_awaiting_friend()
    await t.test_get_awaiting_friend()
    await t.test_get_connection_between_existing_friends()
    await t.test_get_connection_between_not_existing_friends()
    await t.test_update_connection_between_existing_friends()
    await t.test_update_connection_between_not_existing_friends()
    await t.test_get_recommendations_for_user()


if __name__ == '__main__':
    asyncio.run(main())
