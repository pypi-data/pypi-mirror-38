from .properties import BaseProperty


class ObjectProperty(BaseProperty):
    """
    Stores a object property.
    """

    def __init__(self, obj_type, **kwargs):
        """
        Store a dict of values, optionally of a specific type.

        :param obj_type: The type of the object being parsed.
        """
        from simple_mappers.map_definition import MapDefinition
        # values item type
        if obj_type is None:
            raise ValueError("obj_type can not be None.")

        if not issubclass(obj_type, (MapDefinition,)):
            raise TypeError(
                'Expecting Simple Mapper MapDefinition. Got: {}'.format(obj_type)
            )

        self.obj_type = obj_type
        super(ObjectProperty, self).__init__(**kwargs)

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        value = super().inflate(value)
        if value is None:
            return None
        
        from simple_mappers.map_definition import MapDefinition
        
        if isinstance(value, dict):
            obj = self.obj_type.from_dict(value)
        elif isinstance(value, MapDefinition):
            obj = self.obj_type.from_object(value)
        else:
            obj = self.obj_type.from_object(value)
            
        return obj

    def deflate(self, value, **kwargs):
        """Returns the value that should be used to send to the object being mapped."""
        value = self.obj_type.deflate(value)
        value = super().deflate(value)
        return value
