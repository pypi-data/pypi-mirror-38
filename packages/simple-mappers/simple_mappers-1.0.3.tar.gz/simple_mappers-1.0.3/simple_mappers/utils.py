"""
Utils module - A collection of utility functions used by the SimpleMappers framework.
"""


def get_object_attrs(obj):
    """
    Builds a dictionary containing the object properties that are not 'private' (starting with '__')
    or 'protected' (starting with '_'). Functions and callable objects are not included too.
    """
    properties = dict()
    # a list of all object attributes
    property_names = dir(obj)
    # foreach attribute name
    for p_name in property_names:
        # filter the public attributes
        if not p_name.startswith('_'):
            prop = getattr(obj, p_name)
            # filter functions and callable objects
            if not callable(prop) and not isinstance(getattr(obj.__class__, p_name, None), property):
                properties[p_name] = prop

    return properties