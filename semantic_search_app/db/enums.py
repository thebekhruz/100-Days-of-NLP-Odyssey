# enums.py
from enum import Enum, auto


class EntityType(Enum):
    DOCUMENT = auto()
    PERSON = auto()
    LOCATION = auto()
    ORGANISATION = auto()
    MISCELLANEOUS = auto()
    DATE = auto()


class RelationshipType(Enum):
    MENTIONS = auto()
    MENTIONED_ON = auto()
    LOCATED_IN = auto()


RELATIONSHIP_MAPPINGS = {
    EntityType.DOCUMENT: {
        RelationshipType.MENTIONS: [EntityType.PERSON, EntityType.LOCATION, EntityType.ORGANISATION, EntityType.MISCELLANEOUS],
        RelationshipType.MENTIONED_ON: [EntityType.DATE],
    },
    EntityType.PERSON: {
        RelationshipType.MENTIONED_ON: [EntityType.DATE],
    },
    EntityType.LOCATION: {
        RelationshipType.MENTIONED_ON: [EntityType.DATE],
    },
    EntityType.ORGANISATION: {
        RelationshipType.LOCATED_IN: [EntityType.LOCATION],
        RelationshipType.MENTIONED_ON: [EntityType.DATE],
    },
    EntityType.MISCELLANEOUS: {
        RelationshipType.MENTIONED_ON: [EntityType.DATE],
    },
    # Add other mappings as necessary
}


