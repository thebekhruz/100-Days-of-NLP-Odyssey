# from db.enums import EntityType
from neomodel import StringProperty, IntegerProperty


class ModelUtils:
    def __init__(self):
        pass

    def get_attributes_for_model(model_class):
        # Lists all StringProperty and IntegerProperty attributes of a model class
        attributes = [
            prop_name
            for prop_name, prop_obj in model_class.__dict__.items()
            if isinstance(prop_obj, (StringProperty, IntegerProperty))
        ]
        return attributes

    def get_model_class(self, entity_type):
        from db.models import (
            DOCUMENT,
            PERSON,
            LOCATION,
            ORGANISATION,
            MISCELLANEOUS,
            DATE,
        )

        print(entity_type)
        """
        Maps an EntityType to its corresponding model class.

        Args:
            entity_type (EntityType): An enum value representing the entity type.

        Returns:
            The corresponding model class.
        """
        if entity_type == EntityType.DOCUMENT:
            return DOCUMENT
        elif entity_type == EntityType.PERSON:
            return PERSON
        elif entity_type == EntityType.LOCATION:
            return LOCATION
        elif entity_type == EntityType.ORGANISATION:
            return ORGANISATION
        elif entity_type == EntityType.MISCELLANEOUS:
            return MISCELLANEOUS
        elif entity_type == EntityType.DATE:
            return DATE
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
