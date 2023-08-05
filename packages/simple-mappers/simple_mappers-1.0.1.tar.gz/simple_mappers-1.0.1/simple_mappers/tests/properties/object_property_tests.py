"""A test suite for the ObjectProperty test module."""
import unittest
from simple_mappers import properties
from simple_mappers.properties.mapping_error import RequiredPropertyError, InvalidAttributeValueError
from simple_mappers import JsonObject
from simple_mappers import MapDefinition


class TestClass(MapDefinition):

    val1 = properties.StringProperty()
    val2 = properties.StringProperty()
    val3 = properties.StringProperty(mapping_from="vv", norm_func=lambda x:str(x).upper())


class ObjectPropertyTests(unittest.TestCase):
    """
    Test suite for the BaseProperty class.
    """

    def test_should_inflate_property_from_dict(self):
        prop = properties.ObjectProperty(obj_type=TestClass)
        _inputs = {'val1':2,'val2':2}
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, TestClass))
        self.assertTrue(val.val1 == '2')
        self.assertTrue(val.val2 == '2')

        val = prop.inflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_property_from_object(self):
        prop = properties.ObjectProperty(obj_type=TestClass)
        _inputs = JsonObject(**{'val1': 2, 'val2': 2})
        val = prop.inflate(_inputs)

        self.assertTrue(isinstance(val, TestClass))
        self.assertTrue(isinstance(val.val1, str))
        self.assertTrue(isinstance(val.val2, str))

        self.assertTrue(val.val1 == '2')
        self.assertTrue(val.val2 == '2')

    def test_should_inflate_property_from_mapping_definition(self):
        prop = properties.ObjectProperty(obj_type=TestClass)
        _inputs = TestClass.from_dict({'val1': 2, 'val2': 2})
        val = prop.inflate(_inputs)
        self.assertTrue(isinstance(val, TestClass))
        self.assertTrue(isinstance(val.val1, str))
        self.assertTrue(isinstance(val.val2, str))

        self.assertTrue(val.val1 == '2')
        self.assertTrue(val.val2 == '2')

    def test_should_inflate_map_and_normalize_property(self):
        _inputs = TestClass.from_dict({"vv":"test_norm_str"})
        self.assertTrue(_inputs.val3 == "TEST_NORM_STR")

        _inputs = TestClass.from_dict({"vv":"test_norm_str"})
        self.assertTrue(_inputs.val3 == "TEST_NORM_STR")

    def test_should_build_dict_from_property(self):
        prop = properties.ObjectProperty(obj_type=TestClass)
        value = TestClass.from_dict({'val1': "informações", 'val2': 2})
        result = prop.deflate(value)

        self.assertTrue(type(result) == dict)
        expected = {'val2': '2', 'val3': None, 'val1': 'informações'}
        self.assertTrue(expected == result)

if __name__ == "__main__":
    unittest.main()