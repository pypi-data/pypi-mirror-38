from . import BaseProperty


class ComposedProperty(BaseProperty):
    """
    Composite attribute type.
    """

    def __init__(self, compose_function, attr_list, attr_type=None, itens_type=None, **kwargs):
        """
        Composite attribute type.

        :param compose_function: a function to compose the attribute
        :param attr_list: A Pre-defined list of attributes.
        :param attr_type: attribute type mapping.
        :param itens_type: composed property itens type.
        """
        # values item type
        if compose_function is None or not callable(compose_function):
            raise ValueError(
                'You must pass a compose_function to use the compose attribute type.'
                'Got {}'.format(type(compose_function))
            )

        # values item type
        # if attr_list is None or len(attr_list) == 0:
        #     raise ValueError(
        #         'You must pass the attr_list parameter to use the compose attribute type.'
        #         'attr_list is a list of attribute_names that should be used to compose the new attribute.'
        #     )

        self.attr_list = attr_list
        self.compose = compose_function
        self.attr_type = attr_type
        self.itens_type = itens_type
        super(ComposedProperty, self).__init__(**kwargs)

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""

        value = super().inflate(value)
        if not value:
            return None

        if isinstance(value, dict):
            return self.inflate_from_dict(value)
        elif isinstance(value, (list, tuple)):
            return self.inflate_from_list(value)
        elif isinstance(value, object):
            return self.inflate_from_object(value)

    def inflate_from_dict(self, value):
        """inflates a dictionary from other dictionary"""
        attr_vals = list()
        if self.attr_list is None:
            raise AttributeError(
                "It is expected that the attr_list of property names is defined when deflating from an dictionary,"
                "but we got None instead."
            )
        # for each attr_name in the attr_list
        for attr_name in self.attr_list:
            # get the attr value  and saves it in a result list
            val = value.get(attr_name, None)
            # cehck when there is a itens type definition
            if self.itens_type:
                # calls inflate method of the item type definition
                val = self.itens_type.inflate(val)
            # appends to the result list
            attr_vals.append(val)
        # apply composite function
        val = self.compose(*attr_vals)
        # checks when it is defined an attr_type for the result value returned by the compose function
        if self.attr_type:
            val = self.attr_type.inflate(val)
        # return the result value
        return val

    def inflate_from_list(self, value):
        # sannity check in attr_list length and type
        if self.attr_list is None or len(value) != len(self.attr_list):
            raise AttributeError(
                "It is expected that the attr_list of property names is defined when deflating from an dictionary,"
                "but we got None instead."
            )
        # if every thing is fine than performs the inflate
        elif len(value) == len(self.attr_list):
            if self.itens_type:
                res_list = [self.itens_type.inflate(v) for v in value]
            else:
                res_list = [value[i] for i in self.attr_list]
            res = self.compose(*res_list)

            if self.attr_type:
                res = self.attr_type.inflate(res)

            return res
        else:
            raise ValueError(
                "Cant compose attribute from a lists that has more items than the number of defined compose attributes."
            )

    def inflate_from_object(self, value):
        vals = list()

        for attr_name in self.attr_list:
            val = getattr(value, attr_name, None)
            if self.itens_type:
                val = self.itens_type.inflate(val)
            vals.append(val)
        val = self.compose(*vals)

        if self.attr_type:
            val = self.attr_type.inflate(val)
        return val

    def deflate(self, value, **kwargs):
        """Returns the value that should be used to send to the object being mapped."""
        return value
