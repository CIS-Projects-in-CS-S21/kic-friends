import logging

import grpclib
from grpclib import GRPCError, Status

from proto.friends_pb2 import *
from proto.friends_grpc import *
from friends.data.friendslist.repository import Repository

logger = logging.getLogger(__name__)


class FriendsService(FriendsBase):

    def __init__(self, repo: Repository):
        self.db = repo

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

    ######## RPC Handlers ########

    async def GetFriendsForUser(self,
                                stream: 'grpclib.server.Stream['
                                        'GetFriendsForUserRequest, '
                                        'GetFriendsForUserResponse]'
                                ) -> None:
        request = await stream.recv_message()
        res = self.get_user_friends_from_cache(request)
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

    async def GetAwaitingFriendsForUser(self,
                                        stream: 'grpclib.server.Stream['
                                                'GetFriendsForUserRequest, '
                                                'GetFriendsForUserResponse]'
                                        ) -> None:
        request = await stream.recv_message()
        res = self.get_user_awaiting_friends_from_cache(request)
        await stream.send_message(res)

    async def AddAwaitingFriend(self,
                                stream: 'grpclib.server.Stream['
                                        'AddAwaitingFriendRequest, '
                                        'AddAwaitingFriendResponse]'
                                ) -> None:
        logger.debug("Received request to CreateConnectionForUsers")
        request = await stream.recv_message()
        res = self.add_awaiting_friend_to_cache(request)
        await stream.send_message(res)
