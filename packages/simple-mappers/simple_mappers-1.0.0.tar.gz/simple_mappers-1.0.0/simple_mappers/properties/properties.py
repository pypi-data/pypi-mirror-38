"""
properties module - defines class properties attributes.
"""
import collections
import datetime
import pytz
import json
from .mapping_error import RequiredPropertyError, InvalidAttributeValueError


class BaseProperty(object):
    """
    Base class for object properties
    """

    def __init__(self, required=False, default=None, mapping_from=None, mapping_to=None, cascade=True, **kwargs):
        """
        A Base class property definition. 
        :param required: True if the attribute is required.
                         When true and it is not possible to map the attribute from the other object,
                         it raises a value error exception. 
        :param default: default value or function generator.
        :param mapping_name: the name of the attribute in the other object
        :param cascade: when true mappers try to map the the property from the other object properties.
        :param kwargs:
        """
        if default is not None and required:
            raise ValueError("required and default arguments are mutually exclusive")

        self.required = required
        self.default = default
        self.has_default = True if self.default is not None else False

        self.mapping_from = mapping_from  # define the name of the property in the database
        self.mapping_to = mapping_to  # define the name of the property in the database
        self.cascade = cascade
        # auto filled property
        self.property_name = ""
        self.validate = kwargs.get("validate_func", None)

    def default_value(self):
        """
        Generate a default value

        :return: the value
        """
        if self.has_default:
            if callable(self.default):
                return self.default()
            else:
                return self.default
        else:
            return None

    def inflate(self, value):
        """
        returns default or value. 
        """
        # applies the validation function
        if self.validate is not None:
            if not self.validate(value):
                raise InvalidAttributeValueError(
                    "The '{0}' property value '{1}' isn't a valid format for the property '{0}'.".format(
                        self.property_name, value
                    )
                )

        if isinstance(value, str):
            aux = value.lower()
            if aux == 'null' or aux == 'none':
                value = None

        if value is None and self.has_default:
            return self.default_value()
        elif (value is None or value == "") and self.required:
            raise RequiredPropertyError(
                "The {} property is marked as required but no value was given.".format(self.property_name)
            )
        else:
            return value

    def deflate(self, value):
        """
        returns default or value. 
        """
        if value is None:
            return self.default_value()
        else:
            return value


class ChoiceProperty(BaseProperty):
    """
    Defines a base choosable base property.
    """

    def __init__(self, choices=None, should_revert=False, **kwargs):
        """
        Choice property type initialization.
        :param choices: a list of possible string values.
                        or a dict mapping the possible incoming values to its transformed values.
        
        :param should_revert: a boolean that indicates when a mapping should be reverted 
                              in the deflating process. **Default**: False
        
        :param **kwargs required: True if the attribute is required.
                         When true and it is not possible to map the attribute from the other object,
                         it raises a value error exception. 
        :param **kwargs default: default value or function generator.
        :param **kwargs source_name: the name of the attribute in the other object
        """
        super(ChoiceProperty, self).__init__(**kwargs)
        self.should_revert = should_revert
        # if choices
        if choices is not None:
            # sanity type check in choices
            if not isinstance(choices, (tuple, list, dict)):
                raise TypeError("Choices must be a tuple, a list or a dict.")
            # if choices is a dict map
            # then saves the mapping dictionary
            if isinstance(choices, dict):
                self.choices = choices.keys()
                self.choice_map = choices
                # choices reverse map
                self.choice_reverse_map = dict(zip(
                    self.choice_map.values(),
                    self.choice_map.keys()
                ))
            else:  #
                self.choices = choices
                self.choice_map = None
                self.choice_reverse_map = None
        else:
            self.choices = None
            self.choice_map = None
            self.choice_reverse_map = None

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        value = super().inflate(value)

        if self.choice_map:
            if value not in self.choice_map:
                raise InvalidAttributeValueError(
                    "Invalid attribute value {}."
                    " Possible values are {}.".format(value, self.choices)
                )

            return self.choice_map[value]
        elif self.choices:
            if value not in self.choices:
                raise InvalidAttributeValueError(
                    "Invalid attribute value {}."
                    " Possible values are {}.".format(value, self.choices)
                )
        return value

    def deflate(self, value):
        """Returns the value that should be used to send to the object being mapped."""
        value = super().deflate(value)

        if self.choice_map:
            if value not in self.choice_reverse_map:
                raise ValueError(
                    "Invalid attribute value {}."
                    " Possible values are {}.".format(value, self.choice_reverse_map.keys())
                )
            # check when the property value should be reverted by applying a reverse map
            if self.should_revert:
                return self.deflate_revert(value)
            else:  # deflates the raw property value otherwise
                return value
        # check when the property value is in the allowed property values list (called choices).
        elif self.choices and value not in self.choices:
            raise ValueError(
                "Invalid attribute value {}."
                " Possible values are {}.".format(value, self.choices)
            )
        # deflates the raw property value otherwise
        return value

    def deflate_revert(self, value):
        return self.choice_reverse_map[value]


class NormalProperty(BaseProperty):
    """
    Base class for normalized properties.
    """

    def __init__(self, norm_func=None, denorm_func=None, **kwargs):
        """
        Normal property type initialization.
        :param norm_func: a value normalization function.
        :param denorm_func: a value denormalization function.
        """
        super(NormalProperty, self).__init__(**kwargs)
        self.normalize = norm_func
        self.denormalize = denorm_func

    def inflate(self, value):
        """
        returns the normalized property value
        """
        value = super().inflate(value)

        if value is None:
            return None
        else:
            if self.normalize is not None:
                value = self.normalize(value)
                return super().inflate(value)
            else:
                return value

    def deflate(self, value):
        """
        returns the normalized property value
        """
        value = super().deflate(value)
        if value is None:
            return None
        if self.denormalize is not None:
            return self.denormalize(value)
        else:
            return value


class StringProperty(ChoiceProperty, NormalProperty):
    """
    Defines an string property mapper object.
    """

    def __init__(self, **kwargs):
        """
        String property type initialization.
        :param choices: a list of possible string values.
                        or a dict mapping the possible incoming values to its transformed values.
                        
        :param kwargs required: True if the attribute is required.
                         When true and it is not possible to map the attribute from the other object,
                         it raises a value error exception. 
        :param kwargs default: default value or function generator.
        :param kwargs mapping_name: the name of the attribute in the other object
        """
        super(StringProperty, self).__init__(**kwargs)

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        value = super().inflate(value)

        if value is not None:
            value = str(value)

        return value

    def deflate(self, value):
        """Returns the value that should be used to send to the object being mapped."""
        value = super().deflate(value)

        return value


class IntegerProperty(BaseProperty):
    """
    Stores an Integer value
    """

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        value = super().inflate(value)
        if value is None:
            return None
        if value:
            return int(value)
        return 0

    def deflate(self, value):
        """Returns the value that should be used to send to the object being mapped."""
        value = super().deflate(value)
        if value is None:
            return None
        if value:
            return int(value)
        return 0


class ArrayProperty(BaseProperty):
    """
    Stores a list of items
    """

    def __init__(self, itens_type=None, **kwargs):
        """
        Store a list of values, optionally of a specific type.

        :param itens_type: List item type e.g StringProperty for string
        :type: Property
        """
        from simple_mappers.map_definition import MapDefinition
        # list item type
        if itens_type is not None:

            if not isinstance(itens_type, (BaseProperty,)) and not issubclass(itens_type, (MapDefinition,)):
                raise TypeError('Expecting Simple Mapper Property')

        self.itens_type = itens_type

        super(ArrayProperty, self).__init__(**kwargs)

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        if isinstance(value, list) and len(value) == 0:
            value = None

        value = super().inflate(value)
        if not value:
            return None

        if isinstance(value, collections.Iterable):
            if self.itens_type:
                return [self.itens_type.inflate(item) for item in value]

            return list(value)
        else:
            name = self.mapping_from or self.property_name
            raise TypeError(
                "Property Name: '{0}'.\n"
                "Value: '{1}'.\n"
                "Error: Invalid attribute type {2}. The property value must be a iterable type.".format(
                    name, value, type(value)
                )
            )

    def deflate(self, value):
        """Returns the value that should be used to send to the object being mapped."""
        value = super().deflate(value)
        if value is None or len(value) == 0:
            return None

        if isinstance(value, collections.Iterable):
            if self.itens_type:
                return [self.itens_type.deflate(item) for item in value]

            return list(value)
        else:
            name = self.mapping_to or self.property_name
            raise TypeError(
                "Property name: '{0}'.\n"
                "Value: '{1}'.\n"
                "Error: Invalid attribute type '{2}'. The property value must be a iterable type.".format(
                    name, value, type(value)
                )
            )


class FloatProperty(BaseProperty):
    """
    Store a floating point value
    """

    def inflate(self, value):
        value = super().inflate(value)
        if value is None:
            return None
        return float(value)

    def deflate(self, value):
        value = super().deflate(value)
        if value is None:
            return None
        return float(value)


class BooleanProperty(BaseProperty):
    """
    Stores a boolean value
    """

    def __init__(self, trues_str_list=None, **kwargs):
        super().__init__(**kwargs)

        if trues_str_list:
            self.trues = trues_str_list
        else:
            self.trues = ['true', '1', 't', 'y', 'yes', 's', 'sim']

    def inflate(self, value):
        if isinstance(value, str):
            value = self.bool_parser(value)
        return bool(value)

    def deflate(self, value):
        if isinstance(value, str):
            value = self.bool_parser(value)
        return bool(value)

    def bool_parser(self, s):
        return str(s).lower() in self.trues


class DateProperty(NormalProperty):
    """
    Stores a date
    """

    def __init__(self, mask=None, **kwargs):
        """
        Date property type initialization.
        :param mask: string datetime mask used to parse string dates.
                    or a dict mapping the possible incoming values to its transformed values.

        :param kwargs required: True if the attribute is required.
                         When true and it is not possible to map the attribute from the other object,
                         it raises a value error exception. 
        :param kwargs default: default value or function generator.
        :param kwargs source_name: the name of the attribute in the other object
        """
        super().__init__(**kwargs)
        if mask:
            self.mask = mask
        else:
            self.mask = "%Y-%m-%d"

    def inflate(self, value):
        value = super().inflate(value)
        if value is None or value == '':
            return None
        if isinstance(value, str) and value != '':
            return datetime.datetime.strptime(value, self.mask).date()
        elif isinstance(value, datetime.date):
            return value
        else:
            name = self.mapping_from or self.property_name
            raise TypeError(
                "Value type Error: {0}.\n"
                "On Property: '{1}'.\n"
                "Value: {2}"
                " The value type must be a string or a 'datetime.date' object, got {0}".format(type(value), name, value)
            )

    def deflate(self, value):
        value = super().deflate(value)
        if value is None:
            return None
        if not isinstance(value, datetime.date):
            name = self.mapping_to or self.property_name
            msg = "On property: '{0}'\n" \
                  "Property Value: {1}\n" \
                  "Error: datetime.date object expected, got {1}".format(name, repr(value))
            raise TypeError(msg)

        return value.strftime(self.mask)


class DateTimeProperty(NormalProperty):

    def __init__(self, mask=None, **kwargs):
        """
        Datetime property type initialization.
        :param mask: string datetime mask used to parse string dates.
                    or a dict mapping the possible incoming values to its transformed values.

        :param kwargs required: True if the attribute is required.
                         When true and it is not possible to map the attribute from the other object,
                         it raises a value error exception. 
        :param kwargs default: default value or function generator.
        :param kwargs source_name: the name of the attribute in the other object
        """
        if mask:
            self.mask = mask
        else:
            self.mask = "%d/%m/%Y %H:%M"

        super(DateTimeProperty, self).__init__(**kwargs)

    def inflate(self, value):
        value = super().inflate(value)
        if value is None:
            return None

        if isinstance(value, str):
            return datetime.datetime.strptime(value, self.mask)
        elif isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, (float, int)):
            return datetime.datetime.utcfromtimestamp(value).replace(tzinfo=pytz.utc)
        else:
            name = self.mapping_from or self.property_name
            raise TypeError(
                'On Property: {0}\n'
                'Value: {1}\n'
                'Error: Value Type Error, got {1} cant inflate to datetime.'.format(name, value))

    def deflate(self, value):
        value = super().deflate(value)
        if value is None:
            return None

        if not isinstance(value, datetime.datetime):
            name = self.mapping_to or self.property_name
            msg = "On property: '{0}'\n" \
                  "Property Value: {1}\n" \
                  "Error: datetime.date object expected, got {1}".format(name, repr(value))
            raise TypeError(msg)
        return value.strftime(self.mask)


class JSONProperty(BaseProperty):
    """
    Store a data structure as a JSON string.

    The structure will be inflated when a node is retrieved.
    """

    def __init__(self, *args, **kwargs):
        super(JSONProperty, self).__init__(*args, **kwargs)

    def inflate(self, value):
        value = super().inflate(value)
        if isinstance(value, dict):
            return value
        elif isinstance(value, str):
            return json.loads(value)
        else:
            msg = 'str or dict object expected, got {0}'.format(repr(value))
            raise TypeError(msg)

    def deflate(self, value):
        value = super().deflate(value)
        if not isinstance(value, dict):
            msg = 'str or dict object expected, got {0}'.format(repr(value))
            raise TypeError(msg)

        return value
