import os
import logging

import pymongo

from friends.data.friendslist.repository import Repository

logger = logging.getLogger(__name__)


class MongoRepository(Repository):

    def __init__(self, db_name):
        self.friend_collection = pymongo.MongoClient(os.getenv("MONGO_URI"))[db_name].friends

    def get_awaiting_friends_list_for_uid(self, uid: int) -> "List[int]":
        res = self.friend_collection.find_one({
            "uid": uid
        })
        logger.debug(f"Result of find for uid {uid}: {res}")
        if res is None:
            return list()
        return res["awaiting"]

    def get_friends_list_for_uid(self, uid: int) -> "List[int]":
        res = self.friend_collection.find_one({
            "uid": uid
        })
        logger.debug(f"Result of find for uid {uid}: {res}")
        if res is None:
            return list()
        return res["friends"]

    def add_friend_to_list_for_uid(self, uid: int, friend_uid: int) -> bool:
        res = self.friend_collection.find_one({
            "uid": uid
        })
        logger.debug(f"Result of find for uid {uid}: {res}")
        if res is None:
            self.friend_collection.insert_one({
                "uid": uid,
                "friends": [friend_uid],
                "awaiting": list()
            })
            return True
        else:
            if friend_uid not in res['friends']:
                self.friend_collection.update_one(
                    {"uid": uid},
                    {"$push": {"friends": friend_uid}}
                )
                self.friend_collection.update_one(
                    {"uid": uid},
                    {"$pull": {"awaiting": friend_uid}}
                )
                return True
            else:
                return False

    def delete_friend_for_uid(self, uid: int, friend_uid: int) -> bool:
        result = self.friend_collection.update_one(
            {"uid": uid},
            {"$pull": {"friends": friend_uid}}
        )
        if result.modified_count > 0:
            return True
        return False

    def add_awaiting_friend(self, uid: int, friend_uid: int) -> bool:
        res = self.friend_collection.find_one({
            "uid": uid
        })
        logger.debug(f"Result of find for uid {uid}: {res}")
        if res is None:
            self.friend_collection.insert_one({
                "uid": uid,
                "friends": list(),
                "awaiting": [friend_uid]
            })
            return True
        else:
            if friend_uid not in res['awaiting']:
                self.friend_collection.update_one(
                    {"uid": uid},
                    {"$push": {"awaiting": friend_uid}}
                )
                return True
            else:
                return False

    def delete_awaiting_friend_for_uid(self, uid: int, friend_uid: int) -> bool:
        result = self.friend_collection.update_one(
            {"uid": uid},
            {"$pull": {"awaiting": friend_uid}}
        )
        if result.modified_count > 0:
            return True
        return False
