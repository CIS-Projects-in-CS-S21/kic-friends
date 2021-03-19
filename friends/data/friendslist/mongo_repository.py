import os
import logging

import pymongo

from friends.data.friendslist.repository import Repository

logger = logging.getLogger(__name__)


class MongoRepository(Repository):

    def __init__(self, db_name):
        self.friend_collection = pymongo.MongoClient(os.getenv("MONGO_URI"))[db_name]

    def get_friends_list_for_uid(self, uid: int) -> "List[int]":
        pass

    def add_friend_to_list_for_uid(self, uid: int, friend_uid: int) -> bool:
        pass

    def delete_friend_for_uid(self, uid: int, friend_uid: int) -> bool:
        pass
