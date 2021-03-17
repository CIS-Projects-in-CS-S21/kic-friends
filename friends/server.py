from kic.common import User
from kic.friends import *
from friends.data.friendslist.repository import Repository


class FriendsService(FriendsBase):

    def __init__(self, repo: Repository):
        self.db = repo

    async def get_friends_for_user(
            self, user: "User"
    ) -> "GetFriendsForUserResponse":
        """Request a list of the IDs of all friends of a particular user."""
        try:
            friends = self.db.get_friends_list_for_uid(user.user_id)
        except LookupError as e:
            pass

        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_connection_between_users(
            self, first_user_id: int, second_user_id: int
    ) -> "ConnectionBetweenUsersResponse":
        """
        Request information about the connection between two users, checking
        for existence and strength.
        """

        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_recommendations_for_user(
            self, user: "_common__.User", number_recommendations: int
    ) -> "GetRecommendationsForUserResponse":
        """
        Request a list of given size of users who might be friends of the
        requesting user.
        """

        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def create_connection_for_users(
            self, first_user_id: int, second_user_id: int
    ) -> "CreateConnectionForUsersResponse":
        """Add two users as friends and create a connection between them."""

        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def update_connection_between_users(
            self, first_user_id: int, second_user_id: int, update_value: float
    ) -> "ConnectionBetweenUsersResponse":
        """Update a connection strength between two users."""

        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def delete_connection_between_users(
            self, first_user_id: int, second_user_id: int
    ) -> "DeleteConnectionBetweenUsersResponse":
        """Delete the connection between two users."""

        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)
