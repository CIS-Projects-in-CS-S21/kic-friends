import logging

from neomodel import db, DoesNotExist

from friends.data.friendsgraph.repository import Repository
from friends.data.friendsgraph.models.user_node import User

logger = logging.getLogger(__name__)


class Neo4jRepository(Repository):

    def get_or_create_node(self, uid: int):
        node = User.nodes.get_or_none(UserID=uid)
        if not node:
            return User(
                UserID=uid
            ).save()
        return node

    # this should theoretically never fail in production
    @db.transaction
    def create_connection(self, uid: int, friend_uid: int) -> bool:
        u1 = self.get_or_create_node(uid)
        u2 = self.get_or_create_node(friend_uid)
        u1.friends.connect(u2, {'Strength': 1.0})
        logger.debug(f"u1: {len(u1.friends)}")
        logger.debug(f"u2: {len(u2.friends)}")
        return True

    @db.transaction
    def delete_connection(self, uid: int, friend_uid: int) -> bool:
        try:
            u1 = User.nodes.first(UserID=uid)
            u2 = User.nodes.first(UserID=friend_uid)
        except DoesNotExist as err:
            logger.info(err)
            logger.info(f"User searched for {uid} {friend_uid} but does not exist")
            return False
        u1.friends.disconnect(u2)
        return True

    @db.transaction
    def update_connection(self, uid: int, friend_uid: int, multiplier: float) -> float:
        try:
            u1 = User.nodes.first(UserID=uid)
            u2 = User.nodes.first(UserID=friend_uid)
            conn = u1.friends.relationship(u2)
            conn.Strength *= multiplier
            conn.save()
        except DoesNotExist as err:
            logger.info(err)
            logger.info(f"User searched for {uid} {friend_uid} but does not exist, or no relationship")
            return None
        return conn.Strength

    @db.transaction
    def get_connection(self, uid: int, friend_uid: int) -> float:
        u1 = User.nodes.first(UserID=uid)
        u2 = User.nodes.first(UserID=friend_uid)
        conn = u1.friends.relationship(u2)
        if not conn:
            logger.info(f"User searched for {uid} {friend_uid} but does not exist, or no relationship")
            return None
        return conn.Strength

    @db.transaction
    def get_friends(self, uid: int) -> 'List[int]':
        try:
            user = User.nodes.first(UserID=uid)
        except DoesNotExist as err:
            logger.error(f"Asked to get friends for non-existant user {err}")
            return None
        friend_ids = list()
        logger.debug(f"user friends: {user.friends}")
        for friend in user.friends:
            friend_ids.append(friend.UserID)
        return friend_ids


