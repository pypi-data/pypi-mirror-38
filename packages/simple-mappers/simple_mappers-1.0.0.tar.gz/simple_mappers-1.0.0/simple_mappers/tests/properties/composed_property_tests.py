"""A test suite for the ComposedProperty test module."""
import unittest
from simple_mappers import properties
from simple_mappers.properties.mapping_error import RequiredPropertyError, InvalidAttributeValueError
from simple_mappers import JsonObject


class ComposedPropertyTests(unittest.TestCase):
    """
    Test suite for the BaseProperty class.
    """

    def test_should_inflate_property_from_list(self):
        prop = properties.ComposedProperty(compose_function=lambda x,y: x+y, attr_list=[0,1])
        _inputs = [1,2]
        val = prop.inflate(_inputs)
        self.assertTrue(val == 3)

        val = prop.inflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_property_from_list_in_reverse_order(self):
        prop = properties.ComposedProperty(compose_function=lambda x,y: x-y, attr_list=[1,0])
        _inputs = [1,2]
        val = prop.inflate(_inputs)
        self.assertTrue(val == 1)

    def test_should_inflate_property_from_first_index_in_list(self):
        prop = properties.ComposedProperty(compose_function=lambda x, y: x - y, attr_list=[1, 1])
        _inputs = [1, 2]
        val = prop.inflate(_inputs)
        self.assertTrue(val == 0)

    def test_should_inflate_property_from_list_defining_itens_type(self):
        # the compose function
        def compose_function(x,y):
            self.assertTrue(isinstance(x,int))
            self.assertTrue(isinstance(y,int))
            return x+y
        # property definition
        prop = properties.ComposedProperty(
            compose_function=compose_function,
            attr_list=[0, 1],
            itens_type=properties.IntegerProperty()
        )
        # string inputs must be parsed to int
        _inputs = ["1", "2"]
        val = prop.inflate(_inputs)
        self.assertTrue(val == 3)

    def test_should_inflate_property_from_list_defining_attr_type(self):
        # the compose function
        def compose_function(x,y):
            return str(x+y)
        # property definition
        prop = properties.ComposedProperty(
            compose_function=compose_function,
            attr_list=[0, 1],
            itens_type=properties.IntegerProperty(),
            attr_type=properties.IntegerProperty()
        )
        # string inputs must be parsed to int
        _inputs = ["1", "2"]
        val = prop.inflate(_inputs)
        self.assertTrue(val == 3)
        self.assertTrue(isinstance(val,int))

    def test_should_inflate_property_from_dict(self):
        prop = properties.ComposedProperty(compose_function=lambda x,y: x+y, attr_list=['0','1'])
        _inputs = {'0':1,'1':2}
        val = prop.inflate(_inputs)
        self.assertTrue(val == 3)

        val = prop.inflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_property_from_dict_defining_itens_type(self):
        # the compose function
        def compose_function(x, y):
            self.assertTrue(isinstance(x, int))
            self.assertTrue(isinstance(y, int))
            return x + y

        # property definition
        prop = properties.ComposedProperty(
            compose_function=compose_function,
            attr_list=['1', '2'],
            itens_type=properties.IntegerProperty()
        )
        # string inputs must be parsed to int
        _inputs = {"1":'1', "2":'2'}
        val = prop.inflate(_inputs)
        self.assertTrue(val == 3)

    def test_should_inflate_property_from_dict_defining_attr_type(self):
        # the compose function
        def compose_function(x, y):
            return str(x + y)

        # property definition
        prop = properties.ComposedProperty(
            compose_function=compose_function,
            attr_list=['1', '2'],
            itens_type=properties.IntegerProperty(),
            attr_type=properties.IntegerProperty()
        )
        # string inputs must be parsed to int
        _inputs = {"1":'1', "2":'2'}
        val = prop.inflate(_inputs)
        self.assertTrue(val == 3)
        self.assertTrue(isinstance(val,int))

    def test_should_inflate_property_from_object(self):
        _json = {"val1": 1, 'val2': 2}
        _inputs = JsonObject(**_json)
        prop = properties.ComposedProperty(compose_function=lambda x,y: x+y, attr_list=['val1','val2'])
        val = prop.inflate(_inputs)
        self.assertTrue(val == 3)

        val = prop.inflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_property_from_object_defining_itens_type(self):
        # string inputs must be parsed to int
        _json = {"val1": '1', 'val2': '2'}
        _inputs = JsonObject(**_json)

        # the compose function
        def compose_function(x, y):
            self.assertTrue(isinstance(x, int))
            self.assertTrue(isinstance(y, int))
            return x + y

        # property definition
        prop = properties.ComposedProperty(
            compose_function=compose_function,
            attr_list=['val1', 'val2'],
            itens_type=properties.IntegerProperty()
        )
        val = prop.inflate(_inputs)
        self.assertTrue(val == 3)

    def test_should_inflate_property_from_object_defining_attr_type(self):
        # string inputs must be parsed to int
        _json = {"val1": '1', 'val2': '2'}
        _inputs = JsonObject(**_json)

        # the compose function
        def compose_function(x, y):
            return str(x + y)

        # property definition
        prop = properties.ComposedProperty(
            compose_function=compose_function,
            attr_list=['val1', 'val2'],
            itens_type=properties.IntegerProperty(),
            attr_type=properties.IntegerProperty()
        )
        val = prop.inflate(_inputs)
        self.assertTrue(val == 3)
        self.assertTrue(isinstance(val,int))


if __name__ == "__main__":
    unittest.main()