import logging

from grpclib import GRPCError, Status
from grpclib.client import Channel

from proto.friends_pb2 import *
from proto.friends_grpc import *
from friends.data.friendslist.repository import Repository
from proto.users_grpc import UsersStub
from proto.users_pb2 import GetUserNameByIDRequest

logger = logging.getLogger(__name__)


class FriendsService(FriendsBase):

    def __init__(self, repo: Repository, users_service_url):
        self.db = repo
        self.users_service_url = users_service_url

    def get_user_awaiting_friends_from_cache(self,
                                             req: 'GetFriendsForUserRequest'
                                             ) -> 'GetFriendsForUserResponse':
        uid = req.user.userID
        res = self.db.get_awaiting_friends_list_for_uid(uid)
        return GetFriendsForUserResponse(
            friends=res
        )

    def get_user_friends_from_cache(self,
                                    req: 'GetFriendsForUserRequest'
                                    ) -> 'GetFriendsForUserResponse':
        uid = req.user.userID
        res = self.db.get_friends_list_for_uid(uid)
        return GetFriendsForUserResponse(
            friends=res
        )

    def delete_friend_from_cache(self,
                                 req: 'DeleteConnectionBetweenUsersRequest'
                                 ) -> bool:
        uid1 = req.firstUserID
        uid2 = req.secondUserID
        success1 = self.db.delete_friend_for_uid(uid1, uid2)
        success2 = self.db.delete_friend_for_uid(uid2, uid1)
        return success1 and success2

    def add_friend_to_cache(self,
                            req: 'CreateConnectionForUsersRequest'
                            ) -> 'CreateConnectionForUsersResponse':
        uid1 = req.firstUserID
        uid2 = req.secondUserID
        success1 = self.db.add_friend_to_list_for_uid(uid1, uid2)
        success2 = self.db.add_friend_to_list_for_uid(uid2, uid1)
        return CreateConnectionForUsersResponse(
            success=(success1 and success2)
        )

    def add_awaiting_friend_to_cache(self,
                                     req: 'AddAwaitingFriendRequest'
                                     ) -> 'AddAwaitingFriendResponse':
        uid1 = req.firstUserID
        uid2 = req.secondUserID
        success1 = self.db.add_awaiting_friend(uid1, uid2)
        success2 = self.db.add_awaiting_friend(uid2, uid1)
        return AddAwaitingFriendResponse(
            success=(success1 and success2)
        )

    async def get_usernames_from_user_service(self, auth_token_header: str, friend_ids: 'List[int]'):
        user_names = list()
        async with Channel(self.users_service_url, 50051) as channel:
            client = UsersStub(channel)
            for friend_id in friend_ids:
                try:
                    user_res = await client.GetUserNameByID(
                        GetUserNameByIDRequest(
                            userID=friend_id
                        ),
                        metadata={'authorization': auth_token_header}
                    )
                    if user_res.username != "":
                        user_names.append(user_res.username)
                    else:
                        logger.info(f"No error from user service, but received empty username for uid {friend_id}")
                except GRPCError as error:
                    logger.info(f"User service error: {error.status} {error.message}")
        return user_names


    ######## RPC Handlers ########

    async def GetFriendsUsernamesForUser(self,
                                         stream: 'grpclib.server.Stream['
                                                 'GetFriendsForUserRequest, '
                                                 'GetFriendsUsernamesForUserResponse]'
                                         ) -> None:
        request = await stream.recv_message()
        res = self.get_user_friends_from_cache(request)
        logger.debug(stream.metadata)
        auth = stream.metadata["authorization"]
        user_names = await self.get_usernames_from_user_service(auth, list(res.friends))

        response = GetFriendsUsernamesForUserResponse(
            friends=user_names
        )
        await stream.send_message(response)

    async def GetAwaitingFriendsUsernamesForUser(self, stream: 'grpclib.server.Stream['
                                                               'GetFriendsForUserRequest, '
                                                               'GetFriendsUsernamesForUserResponse]'
                                                 ) -> None:
        request = await stream.recv_message()
        res = self.get_user_awaiting_friends_from_cache(request)
        auth = stream.metadata["authorization"]
        user_names = await self.get_usernames_from_user_service(auth, list(res.friends))

        response = GetFriendsUsernamesForUserResponse(
            friends=user_names
        )
        await stream.send_message(response)

    async def GetFriendsForUser(self,
                                stream: 'grpclib.server.Stream['
                                        'GetFriendsForUserRequest, '
                                        'GetFriendsForUserResponse]'
                                ) -> None:
        request = await stream.recv_message()
        res = self.get_user_friends_from_cache(request)
        await stream.send_message(res)

    async def GetAwaitingFriendsForUser(self,
                                        stream: 'grpclib.server.Stream['
                                                'GetFriendsForUserRequest, '
                                                'GetFriendsForUserResponse]'
                                        ) -> None:
        request = await stream.recv_message()
        res = self.get_user_awaiting_friends_from_cache(request)
        await stream.send_message(res)

    async def GetConnectionBetweenUsers(self,
                                        stream: 'grpclib.server.Stream['
                                                'GetConnectionBetweenUsersRequest, '
                                                'ConnectionBetweenUsersResponse]'
                                        ) -> None:
        pass

    async def GetRecommendationsForUser(self,
                                        stream: 'grpclib.server.Stream['
                                                'GetRecommendationsForUserRequest, '
                                                'GetRecommendationsForUserResponse]'
                                        ) -> None:
        pass

    async def CreateConnectionForUsers(self,
                                       stream: 'grpclib.server.Stream['
                                               'CreateConnectionForUsersRequest, '
                                               'CreateConnectionForUsersResponse]'
                                       ) -> None:
        logger.debug("Received request to CreateConnectionForUsers")
        request = await stream.recv_message()
        res = self.add_friend_to_cache(request)
        await stream.send_message(res)

    async def UpdateConnectionBetweenUsers(self,
                                           stream: 'grpclib.server.Stream['
                                                   'UpdateConnectionBetweenUsersRequest, '
                                                   'ConnectionBetweenUsersResponse]'
                                           ) -> None:
        pass

    async def DeleteConnectionBetweenUsers(self,
                                           stream: 'grpclib.server.Stream['
                                                   'DeleteConnectionBetweenUsersRequest, '
                                                   'DeleteConnectionBetweenUsersResponse]'
                                           ) -> None:
        request = await stream.recv_message()
        success = self.delete_friend_from_cache(request)
        if success:
            await stream.send_message(DeleteConnectionBetweenUsersResponse())
            return
        raise GRPCError(
            Status.NOT_FOUND,
            'Could not find one of the requested users',
            [],
        )

    async def AddAwaitingFriend(self,
                                stream: 'grpclib.server.Stream['
                                        'AddAwaitingFriendRequest, '
                                        'AddAwaitingFriendResponse]'
                                ) -> None:
        logger.debug("Received request to CreateConnectionForUsers")
        request = await stream.recv_message()
        res = self.add_awaiting_friend_to_cache(request)
        await stream.send_message(res)
