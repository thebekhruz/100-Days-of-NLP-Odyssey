from neomodel import (StructuredNode, StringProperty, RelationshipTo,
      RelationshipFrom, StructuredRel, ZeroOrMore, IntegerProperty, UniqueIdProperty)


class MENTIONS_REL(StructuredRel):
    ne_type = StringProperty()
    ne_end = IntegerProperty()
    ne_start = IntegerProperty()


class MENTIONED_ON_REL(StructuredRel):
    ne_type = StringProperty()
    ne_end = IntegerProperty()
    ne_start = IntegerProperty()



class DOCUMENT(StructuredNode):
    text = StringProperty()
    doc_id = StringProperty()

    mentions_person = RelationshipTo('PERSON', 'MENTIONS', cardinality=ZeroOrMore)
    mentions_location = RelationshipTo('LOCATION', 'MENTIONS', cardinality=ZeroOrMore)
    mentions_organisation = RelationshipTo('ORGANISATION', 'MENTIONS', cardinality=ZeroOrMore)
    mentions_miscellaneous = RelationshipTo('MISCELLANEOUS', 'MENTIONS', cardinality=ZeroOrMore)
    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', cardinality=ZeroOrMore)

class PERSON(StructuredNode):
    name = StringProperty()
    wiki_ID = StringProperty()

    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', cardinality=ZeroOrMore)


class LOCATION(StructuredNode):
    name = StringProperty()
    wiki_ID = StringProperty()

    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', cardinality=ZeroOrMore)


class ORGANISATION(StructuredNode):
    name = StringProperty()
    wiki_ID = StringProperty()

    located_in = RelationshipTo('LOCATION', 'LOCATED_IN', cardinality=ZeroOrMore)
    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', cardinality=ZeroOrMore)


class MISCELLANEOUS(StructuredNode):
    name = StringProperty()
    wiki_ID = StringProperty()

    mentioned_on = RelationshipTo('DATE', 'MENTIONED_ON', cardinality=ZeroOrMore)


class DATE(StructuredNode):
    date = StringProperty()



