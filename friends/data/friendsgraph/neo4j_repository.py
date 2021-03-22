import logging

from neomodel import db

from friends.data.friendsgraph.repository import Repository
from friends.data.friendsgraph.models.user_node import User
from friends.data.friendsgraph.models.friend_relationship import Friendship


logger = logging.getLogger(__name__)


class Neo4jRepository(Repository):

    def get_or_create_node(self, uid: int):
        node = User.nodes.get_or_none(UserID=uid)
        if not node:
            return User(
                UserID=uid
            ).save()
        return node

    @db.transaction
    def create_connection(self, uid: int, friend_uid: int):
        u1 = self.get_or_create_node(uid)
        u2 = self.get_or_create_node(friend_uid)
        u1.friends.connect(u2, {'Strength': 1.0})
        logger.debug(f"u1: {len(u1.friends)}")
        logger.debug(f"u2: {len(u2.friends)}")

    @db.transaction
    def delete_connection(self, uid: int, friend_uid: int):
        pass

    @db.transaction
    def update_connection(self, uid: int, friend_uid: int, multiplier: float):
        pass
