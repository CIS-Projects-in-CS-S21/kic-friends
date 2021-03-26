import abc


class Repository(abc.ABC):

    @abc.abstractmethod
    def create_connection(self, uid: int, friend_uid: int) -> bool:
        pass

    @abc.abstractmethod
    def delete_connection(self, uid: int, friend_uid: int) -> bool:
        pass

    @abc.abstractmethod
    def update_connection(self, uid: int, friend_uid: int, multiplier: float) -> float:
        pass

    @abc.abstractmethod
    def get_connection(self, uid: int, friend_uid: int) -> float:
        pass

    @abc.abstractmethod
    def get_friends(self, uid: int) -> 'List[int]':
        pass
