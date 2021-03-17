import abc
from typing import List


class Repository(abc.ABC):

    @abc.abstractmethod
    def get_friends_list_for_uid(self, uid: int) -> "List[int]":
        pass

    @abc.abstractmethod
    def add_friend_to_list_for_uid(self, uid: int) -> bool:
        pass

    @abc.abstractmethod
    def delete_friend_for_uid(self, uid: int, friend_uid: int) -> bool:
        pass
