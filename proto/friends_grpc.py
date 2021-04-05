# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: proto/friends.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import proto.common_pb2
import proto.friends_pb2


class FriendsBase(abc.ABC):

    @abc.abstractmethod
    async def GetFriendsUsernamesForUser(self, stream: 'grpclib.server.Stream[proto.friends_pb2.GetFriendsForUserRequest, proto.friends_pb2.GetFriendsUsernamesForUserResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetAwaitingFriendsUsernamesForUser(self, stream: 'grpclib.server.Stream[proto.friends_pb2.GetFriendsForUserRequest, proto.friends_pb2.GetFriendsUsernamesForUserResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetFriendsForUser(self, stream: 'grpclib.server.Stream[proto.friends_pb2.GetFriendsForUserRequest, proto.friends_pb2.GetFriendsForUserResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetAwaitingFriendsForUser(self, stream: 'grpclib.server.Stream[proto.friends_pb2.GetFriendsForUserRequest, proto.friends_pb2.GetFriendsForUserResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetConnectionBetweenUsers(self, stream: 'grpclib.server.Stream[proto.friends_pb2.GetConnectionBetweenUsersRequest, proto.friends_pb2.ConnectionBetweenUsersResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetRecommendationsForUser(self, stream: 'grpclib.server.Stream[proto.friends_pb2.GetRecommendationsForUserRequest, proto.friends_pb2.GetRecommendationsForUserResponse]') -> None:
        pass

    @abc.abstractmethod
    async def CreateConnectionForUsers(self, stream: 'grpclib.server.Stream[proto.friends_pb2.CreateConnectionForUsersRequest, proto.friends_pb2.CreateConnectionForUsersResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AddAwaitingFriend(self, stream: 'grpclib.server.Stream[proto.friends_pb2.AddAwaitingFriendRequest, proto.friends_pb2.AddAwaitingFriendResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UpdateConnectionBetweenUsers(self, stream: 'grpclib.server.Stream[proto.friends_pb2.UpdateConnectionBetweenUsersRequest, proto.friends_pb2.ConnectionBetweenUsersResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DeleteConnectionBetweenUsers(self, stream: 'grpclib.server.Stream[proto.friends_pb2.DeleteConnectionBetweenUsersRequest, proto.friends_pb2.DeleteConnectionBetweenUsersResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DeleteAwaitingFriendBetweenUsers(self, stream: 'grpclib.server.Stream[proto.friends_pb2.DeleteConnectionBetweenUsersRequest, proto.friends_pb2.DeleteConnectionBetweenUsersResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/kic.friends.Friends/GetFriendsUsernamesForUser': grpclib.const.Handler(
                self.GetFriendsUsernamesForUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.GetFriendsForUserRequest,
                proto.friends_pb2.GetFriendsUsernamesForUserResponse,
            ),
            '/kic.friends.Friends/GetAwaitingFriendsUsernamesForUser': grpclib.const.Handler(
                self.GetAwaitingFriendsUsernamesForUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.GetFriendsForUserRequest,
                proto.friends_pb2.GetFriendsUsernamesForUserResponse,
            ),
            '/kic.friends.Friends/GetFriendsForUser': grpclib.const.Handler(
                self.GetFriendsForUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.GetFriendsForUserRequest,
                proto.friends_pb2.GetFriendsForUserResponse,
            ),
            '/kic.friends.Friends/GetAwaitingFriendsForUser': grpclib.const.Handler(
                self.GetAwaitingFriendsForUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.GetFriendsForUserRequest,
                proto.friends_pb2.GetFriendsForUserResponse,
            ),
            '/kic.friends.Friends/GetConnectionBetweenUsers': grpclib.const.Handler(
                self.GetConnectionBetweenUsers,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.GetConnectionBetweenUsersRequest,
                proto.friends_pb2.ConnectionBetweenUsersResponse,
            ),
            '/kic.friends.Friends/GetRecommendationsForUser': grpclib.const.Handler(
                self.GetRecommendationsForUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.GetRecommendationsForUserRequest,
                proto.friends_pb2.GetRecommendationsForUserResponse,
            ),
            '/kic.friends.Friends/CreateConnectionForUsers': grpclib.const.Handler(
                self.CreateConnectionForUsers,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.CreateConnectionForUsersRequest,
                proto.friends_pb2.CreateConnectionForUsersResponse,
            ),
            '/kic.friends.Friends/AddAwaitingFriend': grpclib.const.Handler(
                self.AddAwaitingFriend,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.AddAwaitingFriendRequest,
                proto.friends_pb2.AddAwaitingFriendResponse,
            ),
            '/kic.friends.Friends/UpdateConnectionBetweenUsers': grpclib.const.Handler(
                self.UpdateConnectionBetweenUsers,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.UpdateConnectionBetweenUsersRequest,
                proto.friends_pb2.ConnectionBetweenUsersResponse,
            ),
            '/kic.friends.Friends/DeleteConnectionBetweenUsers': grpclib.const.Handler(
                self.DeleteConnectionBetweenUsers,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.DeleteConnectionBetweenUsersRequest,
                proto.friends_pb2.DeleteConnectionBetweenUsersResponse,
            ),
            '/kic.friends.Friends/DeleteAwaitingFriendBetweenUsers': grpclib.const.Handler(
                self.DeleteAwaitingFriendBetweenUsers,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.friends_pb2.DeleteConnectionBetweenUsersRequest,
                proto.friends_pb2.DeleteConnectionBetweenUsersResponse,
            ),
        }


class FriendsStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.GetFriendsUsernamesForUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/GetFriendsUsernamesForUser',
            proto.friends_pb2.GetFriendsForUserRequest,
            proto.friends_pb2.GetFriendsUsernamesForUserResponse,
        )
        self.GetAwaitingFriendsUsernamesForUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/GetAwaitingFriendsUsernamesForUser',
            proto.friends_pb2.GetFriendsForUserRequest,
            proto.friends_pb2.GetFriendsUsernamesForUserResponse,
        )
        self.GetFriendsForUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/GetFriendsForUser',
            proto.friends_pb2.GetFriendsForUserRequest,
            proto.friends_pb2.GetFriendsForUserResponse,
        )
        self.GetAwaitingFriendsForUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/GetAwaitingFriendsForUser',
            proto.friends_pb2.GetFriendsForUserRequest,
            proto.friends_pb2.GetFriendsForUserResponse,
        )
        self.GetConnectionBetweenUsers = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/GetConnectionBetweenUsers',
            proto.friends_pb2.GetConnectionBetweenUsersRequest,
            proto.friends_pb2.ConnectionBetweenUsersResponse,
        )
        self.GetRecommendationsForUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/GetRecommendationsForUser',
            proto.friends_pb2.GetRecommendationsForUserRequest,
            proto.friends_pb2.GetRecommendationsForUserResponse,
        )
        self.CreateConnectionForUsers = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/CreateConnectionForUsers',
            proto.friends_pb2.CreateConnectionForUsersRequest,
            proto.friends_pb2.CreateConnectionForUsersResponse,
        )
        self.AddAwaitingFriend = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/AddAwaitingFriend',
            proto.friends_pb2.AddAwaitingFriendRequest,
            proto.friends_pb2.AddAwaitingFriendResponse,
        )
        self.UpdateConnectionBetweenUsers = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/UpdateConnectionBetweenUsers',
            proto.friends_pb2.UpdateConnectionBetweenUsersRequest,
            proto.friends_pb2.ConnectionBetweenUsersResponse,
        )
        self.DeleteConnectionBetweenUsers = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/DeleteConnectionBetweenUsers',
            proto.friends_pb2.DeleteConnectionBetweenUsersRequest,
            proto.friends_pb2.DeleteConnectionBetweenUsersResponse,
        )
        self.DeleteAwaitingFriendBetweenUsers = grpclib.client.UnaryUnaryMethod(
            channel,
            '/kic.friends.Friends/DeleteAwaitingFriendBetweenUsers',
            proto.friends_pb2.DeleteConnectionBetweenUsersRequest,
            proto.friends_pb2.DeleteConnectionBetweenUsersResponse,
        )
