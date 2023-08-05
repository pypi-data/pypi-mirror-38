"""
Map Definition Module: Defines the main class that is able to map attrubtes from one object to other.
"""
from .properties import BaseProperty
from .utils import get_object_attrs
import inspect
import json


class MetaDefinition(type):
    def __new__(mcs, what, bases=None, namespace=None):
        cls = super(MetaDefinition, mcs).__new__(mcs, what, bases, namespace)
        props = cls.get_defined_properties()
        cls.__properties__ = props
        for attr_name, prop in props.items():
            prop.property_name = attr_name

        return cls

    def get_defined_properties(cls) -> dict:
        """
        Builds and returns the object property dictionary.
        """
        props = dict()
        # for each derived class of the current class
        # gets the class public properties attributes and builds a dictionary with them.
        for scls in cls.mro():  # runs in the type resolution order
            for prop_name, prop_instance in scls.__dict__.items():
                if not prop_name.startswith("_"):
                    if issubclass(type(prop_instance), BaseProperty):
                        props[prop_name] = prop_instance  # aways overrides properties
                        prop_instance.property_name = prop_name  # sets the instance property name
                    elif inspect.isclass(prop_instance) and issubclass(prop_instance, MapDefinition):
                        # TODO: Class property to be deprecated
                        props[prop_name] = prop_instance  # aways overrides properties

        return props

BaseMapper = MetaDefinition("BaseMapper", (), {})


class MapDefinition(BaseMapper):
    """
    Base Map definition class.
    """
    # Common methods for handling properties on mapping object.
    cascade = True

    def __init__(self, map_undefined=False, **kwargs):
        """Mapper Initialization function."""
        # builds the object from the kwargs mappings
        kwargs = dict(kwargs)
        for property_name, property_instance in self.properties.items():
            if property_name in kwargs:
                attr_value = property_instance.inflate(kwargs[property_name])
                setattr(self, property_name, attr_value)
                # remove property from kwargs
                del kwargs[property_name]

        if map_undefined:
            # undefined properties last (for magic @prop.setters etc)
            for property_name, property_instance in kwargs.items():
                setattr(self, property_name, property_instance)

    def map(self, map_undefined=False, **kwargs):
        """Maps arguments received in kwargs to the current object attributes."""
        # builds the object from the kwargs mappings
        for property_name, property_instance in self.properties.items():
            # handling mapping names
            if isinstance(property_instance, BaseProperty):
                mapping_name = property_instance.mapping_from or property_instance.property_name
            else:
                mapping_name = property_name
            # when cascade is set to true
            # then the property wil be mapper from a single entry in the kwargs
            if property_instance.cascade:
                # if attrbute name is not in kwargs
                # then handles with default values and different attribute name mappings
                if mapping_name not in kwargs:
                    # then check if the current attribute has a defined default value.
                    attr_value = property_instance.inflate(None)
                    # if it has a defined default value
                    # then set this default value to the object being built
                    # None otherwise
                    setattr(self, property_name, attr_value)
                else:  # else attribute name is in kwargs
                    # then set the attribute name and value to the object being built
                    if not isinstance(kwargs[mapping_name], BaseProperty):
                        attr_value = property_instance.inflate(kwargs[mapping_name])
                        setattr(self, property_name, attr_value)
                    # remove property from kwargs
                    del kwargs[mapping_name]
            # otherwise the property will be mapped from the whole dictionary
            else:
                attr_value = property_instance.inflate(kwargs)
                setattr(self, property_name, attr_value)

        if map_undefined:
            # undefined properties last (for magic @prop.setters etc)
            for property_name, property_instance in kwargs.items():
                setattr(self, property_name, property_instance)

    @property
    def properties(self):
        """Return the list of defined class properties."""
        return self.__properties__

    @classmethod
    def from_dict(cls, json_dict, map_undefined=False):
        """
        Maps a json to a new instance of the object type.
        :param json_dict:  a dictionary object.
        :param map_undefined: if true undefined attributes will be mapped to the object instance.
        :return: a instance of the object.
        """
        instance = cls()
        instance.map(map_undefined=map_undefined, **json_dict)
        return instance

    @classmethod
    def from_json(cls, json_str, map_undefined=False):
        """
        Maps a json to a new instance of the object type.
        :param json_str:  a json string.
        :param map_undefined: if true undefined attributes will be mapped to the object instance.
        :return: a instance of the object.
        """
        json_dict = json.loads(json_str)
        return cls.from_dict(json_dict, map_undefined=map_undefined)

    @classmethod
    def from_object(cls, obj, map_undefined=False):
        """
        Maps the object received as parameter to a new object instance of the current class class. 
        :param obj: an object instance.
        :param map_undefined: if true unmapped attributes will be mapped to the new object instance.
        :return: a instance of the current object type.
        """
        obj_props = get_object_attrs(obj)
        kwargs = dict()
        for prop_name, val in obj_props.items():
            kwargs[prop_name] = val
        instance = cls()
        instance.map(map_undefined=map_undefined, **kwargs)
        return instance

    def to_object(self, obj, remove_nones=False):
        """
        Mapps the current object attributes to a target object.
        :param obj: an target objecct instance.
        """
        # for each mapped properties
        for prop_name, prop_def in self.properties.items():
            # get attr val
            attr_val = getattr(self, prop_name, None)

            if remove_nones and attr_val is None:
                continue

            if attr_val is not None:
                is_class = inspect.isclass(attr_val)
                # check attr mapping name
                if not is_class and prop_def.mapping_to:
                    prop_name = prop_def.mapping_to

                # sanity type check
                if isinstance(attr_val, BaseProperty) or is_class:
                    attr_val = None
            # deflate property value
            attr_val = prop_def.deflate(attr_val)  # TODO when val is a MAPPING DEFINITION CALL TO_OBJECT???
            # set to the target object
            setattr(obj, prop_name, attr_val)

    def to_dict(self, should_map=True, remove_nones=False):
        """
        Returns a json representation of the current object.
        :return: a json object representation of the current object.
        """
        obj = dict()
        # for each mapped properties
        for prop_name, prop_def in self.properties.items():
            # get attr val
            attr_val = getattr(self, prop_name, None)
            if remove_nones and attr_val is None:
                continue
            is_class = inspect.isclass(prop_def)
            # check attr mapping name
            if should_map and not is_class and prop_def.mapping_to:
                prop_name = prop_def.mapping_to

            # sanity type check
            # if not isinstance(attr_val, BaseProperty) and not is_class:
            if not isinstance(attr_val, BaseProperty) and not inspect.isclass(attr_val):
                # deflate property value
                if isinstance(attr_val, MapDefinition):
                    attr_val = attr_val.to_dict(should_map=should_map)
                else:
                    attr_val = prop_def.deflate(attr_val, should_map=should_map)
                obj[prop_name] = attr_val

        return obj

    def to_json(self, should_map=True, remove_nones=False):
        """
        Returns a json string representation of the current object.
        :return: a json string object representation of the current object.
        """
        obj = self.to_dict(should_map=should_map, remove_nones=remove_nones)
        return json.dumps(obj)

    @classmethod
    def inflate(cls, value):
        if value is not None:
            if isinstance(value, dict):
                return cls.from_dict(value)
            elif isinstance(value, cls):
                # when created by the the class initializer,
                # a mapping may be an instance of the current
                # mapping definition and then it will not be inflated again
                return value
            else:
                # when trying to inflate from an object that is not a
                # dict and is not a a object os the current class we try to inflate
                # using the from_object function
                return cls.from_object(value)
        return None

    @staticmethod
    def deflate(value, **kwargs):
        if value is None:
            return None
        should_map = kwargs.get("should_map", False)
        return value.to_dict(should_map=should_map)
