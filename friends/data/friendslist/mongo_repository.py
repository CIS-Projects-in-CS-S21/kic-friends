from friends.data.friendslist.repository import Repository


class MongoRepository(Repository):

    def get_friends_list_for_uid(self, uid: int) -> "List[int]":
        pass

    def add_friend_to_list_for_uid(self, uid: int) -> bool:
        pass

    def delete_friend_for_uid(self, uid: int, friend_uid: int) -> bool:
        pass
