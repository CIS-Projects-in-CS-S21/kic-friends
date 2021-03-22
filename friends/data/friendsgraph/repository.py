import abc


class Repository(abc.ABC):

    @abc.abstractmethod
    def create_connection(self, uid: int, friend_uid: int):
        pass

    @abc.abstractmethod
    def delete_connection(self, uid: int, friend_uid: int):
        pass

    @abc.abstractmethod
    def update_connection(self, uid: int, friend_uid: int, multiplier: float):
        pass
