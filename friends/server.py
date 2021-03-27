import logging

from grpclib import GRPCError, Status
from grpclib.client import Channel

from proto.common_pb2 import User
from proto.friends_pb2 import *
from proto.friends_grpc import *
from friends.data.friendslist.repository import Repository as DBRepo
from friends.data.friendsgraph.repository import Repository as GraphRepo
from friends.data.friendsgraph.friend_finding.friend_finder import FriendFinder
from proto.users_grpc import UsersStub
from proto.users_pb2 import GetUserNameByIDRequest

logger = logging.getLogger(__name__)


class FriendsService(FriendsBase):

    def __init__(self, db_repo: DBRepo, graph_repo: GraphRepo, users_service_url: str):
        self.db = db_repo
        self.graph = graph_repo
        self.users_service_url = users_service_url
        self.friend_finder = FriendFinder(self.graph)

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

    def delete_friend(self,
                      req: 'DeleteConnectionBetweenUsersRequest'
                      ) -> bool:
        uid1 = req.firstUserID
        uid2 = req.secondUserID
        success1 = self.db.delete_friend_for_uid(uid1, uid2)
        success2 = self.db.delete_friend_for_uid(uid2, uid1)
        graph_success = self.graph.delete_connection(uid1, uid2)
        return success1 and success2 and graph_success

    def add_friend(self,
                   req: 'CreateConnectionForUsersRequest'
                   ) -> 'CreateConnectionForUsersResponse':
        uid1 = req.firstUserID
        uid2 = req.secondUserID
        success1 = self.db.add_friend_to_list_for_uid(uid1, uid2)
        success2 = self.db.add_friend_to_list_for_uid(uid2, uid1)
        success3 = self.graph.create_connection(uid1, uid2)
        return CreateConnectionForUsersResponse(
            success=(success1 and success2 and success3)
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
        request = await stream.recv_message()
        strength = self.graph.get_connection(request.firstUserID, request.secondUserID)
        if strength is None:
            raise GRPCError(
                Status.NOT_FOUND,
                'Could not find one of the requested users',
                [],
            )
        res = ConnectionBetweenUsersResponse(
            connectionStrength=strength
        )
        await stream.send_message(res)

    async def GetRecommendationsForUser(self,
                                        stream: 'grpclib.server.Stream['
                                                'GetRecommendationsForUserRequest, '
                                                'GetRecommendationsForUserResponse]'
                                        ) -> None:
        logger.debug("Received request to GetRecommendationsForUser")
        request = await stream.recv_message()
        uid = request.user.userID
        num_recs = request.numberRecommendations
        recs = self.friend_finder.get_recommendations(num_recs, uid)

        user_object_list = list()

        auth = stream.metadata["authorization"]
        user_names = await self.get_usernames_from_user_service(auth, recs)

        if len(user_names) != len(recs):
            raise GRPCError(
                Status.INTERNAL,
                'An inconsistency exists for one or more users',
                [],
            )
        for name, uid in zip(user_names, recs):
            user_object_list.append(
                User(
                    userID=uid,
                    userName=name,
                )
            )

        res = GetRecommendationsForUserResponse(
            recommendations=user_object_list
        )
        await stream.send_message(res)

    async def CreateConnectionForUsers(self,
                                       stream: 'grpclib.server.Stream['
                                               'CreateConnectionForUsersRequest, '
                                               'CreateConnectionForUsersResponse]'
                                       ) -> None:
        logger.debug("Received request to CreateConnectionForUsers")
        request = await stream.recv_message()
        res = self.add_friend(request)
        await stream.send_message(res)

    async def UpdateConnectionBetweenUsers(self,
                                           stream: 'grpclib.server.Stream['
                                                   'UpdateConnectionBetweenUsersRequest, '
                                                   'ConnectionBetweenUsersResponse]'
                                           ) -> None:
        logger.debug("Received request to UpdateConnectionBetweenUsers")
        request = await stream.recv_message()
        uid1 = request.firstUserID
        uid2 = request.secondUserID
        strength = self.graph.update_connection(uid1, uid2, request.updateValue)
        res = ConnectionBetweenUsersResponse(
            connectionStrength=strength
        )
        await stream.send_message(res)

    async def DeleteConnectionBetweenUsers(self,
                                           stream: 'grpclib.server.Stream['
                                                   'DeleteConnectionBetweenUsersRequest, '
                                                   'DeleteConnectionBetweenUsersResponse]'
                                           ) -> None:
        logger.debug("Received request to DeleteConnectionBetweenUsers")
        request = await stream.recv_message()
        success = self.delete_friend(request)
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
