from neomodel import (StructuredNode, StringProperty, RelationshipTo,
      RelationshipFrom, StructuredRel, ZeroOrMore, IntegerProperty, UniqueIdProperty)

from neomodel import config
config.DATABASE_URL = "bolt://neo4j:codingRules@localhost:7687"   

class MENTIONS(StructuredRel):
    ne_type = StringProperty()
    ne_start = IntegerProperty()
    ne_end = IntegerProperty()


class MENTIONED_ON(StructuredRel):
    ne_type = StringProperty()
    ne_end = IntegerProperty()
    ne_start = IntegerProperty()



class DOCUMENT(StructuredNode):
    text = StringProperty()
    doc_id = StringProperty()

    mentions_person = RelationshipTo('PERSON', 'MENTIONS', model=MENTIONS)
    mentions_location = RelationshipTo('LOCATION', 'MENTIONS', model=MENTIONS)
    mentions_organisation = RelationshipTo('ORGANISATION', 'MENTIONS', model=MENTIONS)
    mentions_miscellaneous = RelationshipTo('MISCELLANEOUS', 'MENTIONS', model=MENTIONS)
    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', model=MENTIONED_ON)

class PERSON(StructuredNode):
    name = StringProperty()
    wiki_ID = StringProperty()

    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', model=MENTIONED_ON)


class LOCATION(StructuredNode):
    name = StringProperty()
    wiki_ID = StringProperty()

    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', model=MENTIONED_ON)


class ORGANISATION(StructuredNode):
    name = StringProperty()
    wiki_ID = StringProperty()

    located_in = RelationshipTo('LOCATION', 'LOCATED_IN')
    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', model=MENTIONED_ON)


class MISCELLANEOUS(StructuredNode):
    name = StringProperty()
    wiki_ID = StringProperty()

    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', model=MENTIONED_ON)


class DATE(StructuredNode):
    date = StringProperty()



