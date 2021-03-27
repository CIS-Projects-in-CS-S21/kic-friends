from friends.data.friendsgraph.repository import Repository


class MockGraph(Repository):

    def __init__(self):
        self.adjacency_list = {}

    def create_connection(self, uid: int, friend_uid: int):
        self.adjacency_list.setdefault(uid, {})[friend_uid] = 1.0
        self.adjacency_list.setdefault(friend_uid, {})[uid] = 1.0

    def delete_connection(self, uid: int, friend_uid: int):
        self.adjacency_list.get(uid).pop(friend_uid)
        self.adjacency_list.get(friend_uid).pop(uid)

    def update_connection(self, uid: int, friend_uid: int, multiplier: float):
        self.adjacency_list.setdefault(uid, {})[friend_uid] *= multiplier
        self.adjacency_list.setdefault(friend_uid, {})[uid] *= multiplier
        return self.adjacency_list.setdefault(uid, {})[friend_uid]

    def get_connection(self, uid: int, friend_uid: int):
        return self.adjacency_list.get(uid).get(friend_uid, None)

    def get_friends(self, uid: int) -> 'List[int]':
        return self.adjacency_list.get(uid).keys()
