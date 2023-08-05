"""A test suite for the DictProperty test module."""
import unittest
from simple_mappers import properties
from simple_mappers.properties.mapping_error import RequiredPropertyError, InvalidAttributeValueError
from simple_mappers import JsonObject


class ComposedPropertyTests(unittest.TestCase):
    """
    Test suite for the BaseProperty class.
    """

    def test_should_inflate_property_from_list(self):
        prop = properties.DictProperty()
        _inputs = [['1',2],['2',2]]
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val,dict))
        self.assertTrue(val['1'] == 2)
        self.assertTrue(val['2'] == 2)

        val = prop.inflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_property_from_list_defining_key_type(self):
        prop = properties.DictProperty(key_type=properties.IntegerProperty())
        _inputs = [['1', 2], ['2', 2]]
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(isinstance(list(val.keys())[0], int))
        self.assertTrue(isinstance(list(val.keys())[1], int))

        self.assertTrue(val[1] == 2)
        self.assertTrue(val[2] == 2)

    def test_should_inflate_property_from_list_defining_values_type(self):
        prop = properties.DictProperty(
            key_type=properties.IntegerProperty(),
            values_type=properties.IntegerProperty()
        )
        _inputs = [['1', '2'], ['2', '2']]
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(isinstance(list(val.keys())[0], int))
        self.assertTrue(isinstance(list(val.keys())[1], int))

        self.assertTrue(isinstance(list(val.values())[1], int))
        self.assertTrue(isinstance(list(val.values())[1], int))

        self.assertTrue(val[1] == 2)
        self.assertTrue(val[2] == 2)

    def test_should_inflate_property_from_list_defining_key_list(self):
        prop = properties.DictProperty(
            key_type=properties.IntegerProperty(),
            values_type=properties.IntegerProperty(),
            key_list=['1']
        )
        _inputs = [['1', '2'], ['2', '2']]
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(isinstance(list(val.keys())[0], int))

        self.assertTrue(isinstance(list(val.values())[0], int))
        self.assertTrue(len(val) == 1)

        self.assertTrue(val[1] == 2)

    def test_should_inflate_property_from_dict(self):
        prop = properties.DictProperty()
        _inputs = {'1':2,'2':2}
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val,dict))
        self.assertTrue(val['1'] == 2)
        self.assertTrue(val['2'] == 2)

        val = prop.inflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_property_from_dict_defining_key_type(self):
        prop = properties.DictProperty(key_type=properties.IntegerProperty())
        _inputs = {'1':2,'2':2}
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(isinstance(list(val.keys())[0], int))
        self.assertTrue(isinstance(list(val.keys())[1], int))

        self.assertTrue(val[1] == 2)
        self.assertTrue(val[2] == 2)

    def test_should_inflate_property_from_dict_defining_values_type(self):
        prop = properties.DictProperty(
            key_type=properties.IntegerProperty(),
            values_type=properties.IntegerProperty()
        )
        _inputs = {'1':2,'2':2}
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(isinstance(list(val.keys())[0], int))
        self.assertTrue(isinstance(list(val.keys())[1], int))

        self.assertTrue(isinstance(list(val.values())[1], int))
        self.assertTrue(isinstance(list(val.values())[1], int))

        self.assertTrue(val[1] == 2)
        self.assertTrue(val[2] == 2)

    def test_should_inflate_property_from_dict_defining_key_list(self):
        prop = properties.DictProperty(
            key_type=properties.IntegerProperty(),
            values_type=properties.IntegerProperty(),
            key_list=['1']
        )
        _inputs = {'1':2,'2':2}
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(isinstance(list(val.keys())[0], int))

        self.assertTrue(isinstance(list(val.values())[0], int))
        self.assertTrue(len(val) == 1)

        self.assertTrue(val[1] == 2)

    def test_should_inflate_property_from_object(self):
        prop = properties.DictProperty()

        # string inputs must be parsed to int
        _json = {"val1": 2, 'val2': 2}
        _inputs = JsonObject(**_json)

        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(val['val1'] == 2)
        self.assertTrue(val['val2'] == 2)

        val = prop.inflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_property_from_object_defining_key_type(self):
        prop = properties.DictProperty(key_type=properties.StringProperty())

        # string inputs must be parsed to int
        _json = {"val1": '1', 'val2': '2'}
        _inputs = JsonObject(**_json)

        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(isinstance(list(val.keys())[0], str))
        self.assertTrue(isinstance(list(val.keys())[1], str))

        self.assertTrue(val["val1"] == '1')
        self.assertTrue(val["val2"] == '2')

    def test_should_inflate_property_from_object_defining_values_type(self):
        prop = properties.DictProperty(
            key_type=properties.StringProperty(),
            values_type=properties.IntegerProperty()
        )
        # string inputs must be parsed to int
        _json = {"val1": '1', 'val2': '2'}
        _inputs = JsonObject(**_json)

        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(isinstance(list(val.keys())[0], str))
        self.assertTrue(isinstance(list(val.keys())[1], str))

        self.assertTrue(isinstance(list(val.values())[1], int))
        self.assertTrue(isinstance(list(val.values())[1], int))

        self.assertTrue(val['val1'] == 1)
        self.assertTrue(val['val2'] == 2)

    def test_should_inflate_property_from_object_defining_key_list(self):
        prop = properties.DictProperty(
            key_type=properties.StringProperty(),
            values_type=properties.IntegerProperty(),
            key_list=['val1']
        )
        # string inputs must be parsed to int
        _json = {"val1": '1', 'val2': '2'}
        _inputs = JsonObject(**_json)

        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, dict))
        self.assertTrue(isinstance(list(val.keys())[0], str))

        self.assertTrue(isinstance(list(val.values())[0], int))
        self.assertTrue(len(val) == 1)

        self.assertTrue(val["val1"] == 1)

if __name__ == "__main__":
    unittest.main()