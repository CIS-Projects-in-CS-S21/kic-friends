# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: proto/feed.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import proto.common_pb2
import proto.feed_pb2


class FeedBase(abc.ABC):

    @abc.abstractmethod
    async def GenerateFeedForUser(self, stream: 'grpclib.server.Stream[proto.feed_pb2.GenerateFeedForUserRequest, proto.feed_pb2.GenerateFeedForUserResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/kic.feed.Feed/GenerateFeedForUser': grpclib.const.Handler(
                self.GenerateFeedForUser,
                grpclib.const.Cardinality.UNARY_STREAM,
                proto.feed_pb2.GenerateFeedForUserRequest,
                proto.feed_pb2.GenerateFeedForUserResponse,
            ),
        }


class FeedStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.GenerateFeedForUser = grpclib.client.UnaryStreamMethod(
            channel,
            '/kic.feed.Feed/GenerateFeedForUser',
            proto.feed_pb2.GenerateFeedForUserRequest,
            proto.feed_pb2.GenerateFeedForUserResponse,
        )
