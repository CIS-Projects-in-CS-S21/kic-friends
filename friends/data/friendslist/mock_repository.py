from typing import List

from friends.data.friendslist.repository import Repository


class MockRepository(Repository):

    def __init__(self, starting_db=None):
        if starting_db:
            self.db = starting_db
        else:
            self.db = {}

    def get_friends_list_for_uid(self, uid: int) -> "List[int]":
        if uid in self.db:
            return self.db[uid]
        else:
            return list()

    def add_friend_to_list_for_uid(self, uid: int, friend_uid: int) -> bool:
        if uid in self.db:
            if friend_uid not in self.db[uid]:
                self.db[uid].append(friend_uid)
            else:
                return False
        else:
            self.db[uid] = [friend_uid]
        return True

    def delete_friend_for_uid(self, uid: int, friend_uid: int) -> bool:
        if uid in self.db:
            if friend_uid in self.db[uid]:
                self.db[uid].remove(friend_uid)
            else:
                return False
        return True
