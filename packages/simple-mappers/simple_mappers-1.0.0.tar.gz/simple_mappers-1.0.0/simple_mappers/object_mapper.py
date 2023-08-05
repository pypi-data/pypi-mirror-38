"""
Object Mapper Module - Defines functions classes and functions to create and define simple mappers. 
"""
from .utils import get_object_attrs


class SimpleMapper(object):
    """
    A Simple object to object mapper class definition.
    """

    def __init__(self, properties=None, strict=True, defs_only=False):
        if properties:
            self.properties = properties
        else:
            self.properties = dict()
        self.strict = strict
        self.defs_only = defs_only

    def map(self, source, target):
        """
        A mapping function that gets the properties from a source object and sets in the target attribute.
        :param source: the source object instance. 
        :param target: the target object instance. 
        """
        if self.defs_only:
            self._def_only_map(source, target)
        else:
            obj_dict = get_object_attrs(source)
            for prop_name, prop_val in obj_dict.items():
                if prop_name in self.properties:
                    prop_def = self.properties[prop_name]
                    prop_val = prop_def.deflate(prop_val)
                    if prop_def.mapping_from:
                        prop_name = prop_def.mapping_from

                self._set_attr(target, prop_name, prop_val)

    def _def_only_map(self, source, target):
        """
        A mapping function that only uses the mapper attribute definitions.
        """
        for prop_name, prop_map in self.properties.items():
            prop_val = getattr(source, prop_name, None)
            prop_val = prop_map.deflate(prop_val)
            if prop_map.mapping_from:
                self._set_attr(target, prop_map.mapping_from, prop_val)
            else:
                self._set_attr(target, prop_name, prop_val)

    def _set_attr(self, target, attr_name, attr_val):
        if isinstance(target, dict):
            target[attr_name] = attr_val

        elif self.strict:
            if hasattr(target, attr_name):
                setattr(target, attr_name, attr_val)
        else:
            setattr(target, attr_name, attr_val)

    def map_to_dict(self, source):
        result = dict()


class JsonObject(object):
    """
    A simple parsed Json object.
    """
    def __init__(self, **json_dict):
        json_dict = dict(json_dict)
        for attr_name, attr_val in json_dict.items():
            setattr(self, attr_name, attr_val)

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        elif hasattr(self, item):
            return object.__getattribute__(self, item)
        else:
            return None

    def to_dict(self):
        """
        Recursively inspect all key/values of the given object and builds its dictionary representation.
        :return: a dict representation of the object.
        """
        res = dict()
        attrs = get_object_attrs(self)
        for name, value in attrs.items():
            if isinstance(value, JsonObject):
                value = value.to_dict()
            elif isinstance(value, (dict,)):
                value = self._to_dict(value)
            res[name] = value

        return res

    @staticmethod
    def _to_dict(d:dict):
        res = dict()
        for name, value in list(d.items()):
            if isinstance(value, (dict,)):
                value = JsonObject._to_dict(value)
            elif isinstance(value,(JsonObject,)):
                value = value.to_dict()

            res[name] = value
        return res