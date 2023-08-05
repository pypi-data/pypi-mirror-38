"""
Mapping Error Module - Defines Mapping Errors and Exception classes.
"""


class MappingError(ValueError):
    pass


class RequiredPropertyError(MappingError):
    pass


class InvalidAttributeValueError(MappingError):
    pass