from neomodel import (StructuredNode, StringProperty, RelationshipTo,
                      RelationshipFrom, StructuredRel, ZeroOrMore, IntegerProperty,
                      UniqueIdProperty, config)

# Database configuration should be done elsewhere, e.g., in a separate config file or setup script
config.DATABASE_URL = "bolt://neo4j:codingRules@localhost:7687"

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class BaseRel(StructuredRel):
    ne_type = StringProperty()
    ne_start = IntegerProperty()
    ne_end = IntegerProperty()
    relevance = IntegerProperty()


class MENTIONS(BaseRel):
    pass

class MENTIONED_ON(BaseRel):
    pass

class BaseEntity(StructuredNode):
    name = StringProperty()
    wiki_ID = StringProperty()  # Assuming wiki_ID is unique
    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', model=MENTIONED_ON)

class DOCUMENT(StructuredNode):
    text = StringProperty()
    doc_id = StringProperty(unique_index=True)  # Assuming doc_id is unique
    text_embedding = 

    mentions_person = RelationshipTo('PERSON', 'MENTIONS', model=MENTIONS)
    mentions_location = RelationshipTo('LOCATION', 'MENTIONS', model=MENTIONS)
    mentions_organisation = RelationshipTo('ORGANISATION', 'MENTIONS', model=MENTIONS)
    mentions_miscellaneous = RelationshipTo('MISCELLANEOUS', 'MENTIONS', model=MENTIONS)
    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', model=MENTIONED_ON)


class PERSON(BaseEntity):
    pass

class LOCATION(BaseEntity):
    pass

class ORGANISATION(BaseEntity):
    pass

class MISCELLANEOUS(BaseEntity):
    pass

class DATE(StructuredNode):
    date = StringProperty()
