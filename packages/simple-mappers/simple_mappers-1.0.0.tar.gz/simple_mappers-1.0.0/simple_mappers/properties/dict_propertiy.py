from . import BaseProperty


class DictProperty(BaseProperty):
    """
    Stores a dict of items
    """

    def __init__(self, values_type=None, key_type=None, key_list=None, **kwargs):
        """
        Store a dict of values, optionally of a specific type.

        :param values_type: Dict values type e.g StringProperty for string
        :param key_type: Dict keys type e.g StringProperty for string
        :param key_list: A Pre-defined list of the dictionary keys
        """
        from simple_mappers.map_definition import MapDefinition
        # values item type
        if values_type is not None:
            if not isinstance(values_type, (BaseProperty,)) and not issubclass(values_type, (MapDefinition,)):
                raise TypeError(
                    'Expecting Simple Mapper Property. Got: {}'.format(type(values_type))
                )

        # values item type
        if key_type is not None:
            if not isinstance(key_type, (BaseProperty,)) and not issubclass(key_type, (MapDefinition,)):
                raise TypeError(
                    'Expecting Simple Mapper Property. Got: {}'.format(type(key_type))
                )

        self.values_type = values_type
        self.key_type = key_type
        self.key_list = key_list

        super(DictProperty, self).__init__(**kwargs)

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        value = super().inflate(value)
        if value is None:
            return None

        if isinstance(value, dict):
            return self.inflate_from_dict(value)
        elif isinstance(value, (list, tuple)):
            return self.inflate_from_list(value)
        elif isinstance(value, object):
            return self.inflate_from_object(value)

    def inflate_from_dict(self, value):
        """inflates a dictionary from other dictionary"""
        # when there is a pre defined key list
        # then checks when the key is in the list before inserting in the new dictionary
        if self.key_list:
            if self.values_type and self.key_type:
                return {
                    self.key_type.inflate(key): self.values_type.inflate(val)
                    for key, val in value.items() if key in self.key_list
                }
            elif self.values_type:
                return {
                    key: self.values_type.inflate(val)
                    for key, val in value.items() if key in self.key_list
                }
            elif self.key_type:
                return {
                    self.key_type.inflate(key): val
                    for key, val in value.items() if key in self.key_list
                }
            else:
                return {
                    key: val
                    for key, val in value.items() if key in self.key_list
                }
        # otherwise builds a new dictionary with all keys and values
        else:
            if self.values_type and self.key_type:
                return {self.key_type.inflate(key): self.values_type.inflate(val) for key, val in value.items()}
            elif self.values_type:
                return {key: self.values_type.inflate(val) for key, val in value.items()}
            elif self.key_type:
                return {self.key_type.inflate(key): val for key, val in value.items()}
            else:
                return value

    def inflate_from_list(self, value):
        try:
            if self.key_list:
                # check when values and key types are sett
                return self.inflate_from_list_checking_pre_defs(value)
            else:
                return self.inflate_from_list_no_pre_defs(value)
        except IndexError:
            name = self.mapping_from or self.property_name
            raise TypeError(
                "On property: {}.\n"
                "Value: {}.\n"
                "Error: cannot convert sequence into a dictionary. "
                "It is expected that the length of each element of the list/tuple"
                "to be 2.".format(name, value)
            )

    def inflate_from_list_checking_pre_defs(self, value):
        """
        inflates a dictionary object when a pre-defined list of keys is defined.
        :param value: the list object to inflate from
        :return: the inflated dict
        """
        # check when values and key types are sett
        if self.values_type and self.key_type:
            return {
                self.key_type.inflate(val[0]): self.values_type.inflate(val[1])
                for val in value if val[0] in self.key_list
            }
        # check when only value type is set
        elif self.values_type:
            return {
                val[0]: self.values_type.inflate(val[1])
                for val in value if val[0] in self.key_list
            }
        # check when only key type is set
        elif self.key_type:
            return {
                self.key_type.inflate(val[0]): val[1]
                for val in value if val[0] in self.key_list
            }
        # otherwise, default behavior
        else:
            return {val[0]: val[1] for val in value if val[0] in self.key_list}

    def inflate_from_list_no_pre_defs(self, value):
        """inflates a dictionary from a list of object when there is no pre defined key."""
        if self.values_type and self.key_type:
            return {
                self.key_type.inflate(val[0]): self.values_type.inflate(val[1])
                for val in value
            }
        # check when only value type is set
        elif self.values_type:
            return {
                val[0]: self.values_type.inflate(val[1])
                for val in value
            }
        # check when only key type is set
        elif self.key_type:
            return {
                self.key_type.inflate(val[0]): val[1]
                for val in value
            }
        # otherwise default behavior
        else:
            return dict(value)

    def inflate_from_object(self, value):
        # check for pre defined keys
        if self.key_list:
            # # inflates when the dictionary when predefined keys are set
            m_result = dict()
            for key in self.key_list:
                self.inflate_from_object_attribute(key, value, m_result)
            return m_result
        else:  # there is no pre defined keys
            # inflates when there is no predefined keys
            from simple_mappers.utils import get_object_attrs
            attr_names = get_object_attrs(value)
            m_result = dict()
            for name in attr_names.keys():
                self.inflate_from_object_attribute(name, value, m_result)
            return m_result

    def inflate_from_object_attribute(self, key, value, m_result):
        """inflates a dict entry with an object attribute."""

        if self.key_type:
            k = self.key_type.inflate(key)
        else:
            k = key
        # if object has an attribute with the current key name,
        # then add a key value pair to the dict
        if hasattr(value, key):
            if self.values_type:
                # when it has a defined value type we must deflate the value recovered from the object
                val = self.values_type.inflate(getattr(value, key))
            else:
                # else we just get the current object attribute value
                val = getattr(value, key)
            # add key value pair to the dictionary
            m_result[k] = val

    def deflate(self, value):
        """Returns the value that should be used to send to the object being mapped."""
        return value
