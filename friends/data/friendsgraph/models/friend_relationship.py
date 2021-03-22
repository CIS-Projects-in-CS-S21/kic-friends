from neomodel import StructuredRel, FloatProperty


class Friendship(StructuredRel):
    Strength = FloatProperty(required=True)
