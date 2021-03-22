from neomodel import StructuredNode, Relationship, IntegerProperty

from friends.data.friendsgraph.models.friend_relationship import Friendship


class User(StructuredNode):
    UserID = IntegerProperty(required=True)
    friends = Relationship('User', 'FRIEND', model=Friendship)
