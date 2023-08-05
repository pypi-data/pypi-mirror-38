"""A Test suite for the properties.py module."""
import unittest
from simple_mappers import properties
from simple_mappers.properties.mapping_error import RequiredPropertyError, InvalidAttributeValueError


class BasePropertyTests(unittest.TestCase):
    """
    Test suite for the BaseProperty class.
    """

    def test_should_inflate_property(self):
        prop = properties.BaseProperty()

        val = prop.inflate("test")
        self.assertTrue(val == "test")

        val = prop.inflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_default_value(self):
        prop = properties.BaseProperty(default="33")
        val = prop.inflate(None)
        self.assertTrue(val == "33")
        prop = properties.BaseProperty(default=lambda : 22)
        val = prop.inflate(None)
        self.assertTrue(val == 22)

    def test_should_deflate_value(self):
        prop = properties.BaseProperty()

        val = prop.deflate("test")
        self.assertTrue(val == "test")

        val = prop.deflate(None)
        self.assertTrue(val is None)

    def test_should_deflate_default_value(self):

        prop = properties.BaseProperty(default="33")
        val = prop.deflate(None)
        self.assertTrue(val == "33")
        prop = properties.BaseProperty(default=lambda : 22)
        val = prop.deflate(None)
        self.assertTrue(val == 22)

        self.assertTrue(prop.has_default)

    def test_should_raise_error(self):
        prop = properties.BaseProperty(required=True)
        self.assertRaises(RequiredPropertyError, prop.inflate, None)

    def test_should_map_string_valued_with_null_to_none(self):
        prop = properties.BaseProperty()
        val = prop.inflate('None')
        self.assertTrue(val is None)
        val = prop.inflate('null')
        self.assertTrue(val is None)
        val = prop.inflate('Null')
        self.assertTrue(val is None)


class ChoicePropertyTests(unittest.TestCase):

    def test_should_accept_values_from_list(self):

        prop = properties.ChoiceProperty(['1', '2', '3'])

        val = prop.inflate('1')
        self.assertTrue('1' == val)
        val = prop.inflate('2')
        self.assertTrue('2' == val)
        val = prop.inflate('3')
        self.assertTrue('3' == val)

    def test_should_raise_invalid_attribute_error(self):
        prop = properties.ChoiceProperty(['1', '2', '3'])
        self.assertRaises(InvalidAttributeValueError, prop.inflate, '6')

    def test_should_accept_values_from_tuple(self):

        prop = properties.ChoiceProperty(('1', '2', '3'))

        val = prop.inflate('1')
        self.assertTrue('1' == val)
        val = prop.inflate('2')
        self.assertTrue('2' == val)
        val = prop.inflate('3')
        self.assertTrue('3' == val)

    def test_should_map_to_dict_values(self):

        prop = properties.ChoiceProperty({'1': '2', '3':'5'})

        val = prop.inflate('1')
        self.assertTrue('2' == val)
        val = prop.inflate('3')
        self.assertTrue('5' == val)

    def test_should_raise_error(self):
        prop = properties.ChoiceProperty({'1': '2', '3': '5'})
        self.assertRaises(InvalidAttributeValueError, prop.inflate, '7')


class NormalPropertyTests(unittest.TestCase):

    def test_should_normalize_string(self):
        prop = properties.NormalProperty(norm_func=lambda x: str(x).strip())

        val = prop.inflate('  str_str  ')
        self.assertTrue('str_str' == val)
        val = prop.inflate(None)
        self.assertTrue(None == val)


class StringPropertyTests(unittest.TestCase):

    def test_should_inflate_int(self):
        prop = properties.StringProperty()

        val = prop.inflate(1)
        self.assertTrue('1' == val)

    def test_should_inflate_float(self):
        prop = properties.StringProperty()

        val = prop.inflate(1.3)
        self.assertTrue('1.3' == val)

    def test_should_inflate_None(self):
        prop = properties.StringProperty()

        val = prop.inflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_simple_string(self):

        prop = properties.StringProperty()

        val = prop.inflate("xpto")
        self.assertTrue(val == "xpto")

        val = prop.inflate(None)

        self.assertTrue(val is None)

    def test_should_deflate_simple_string(self):
        prop = properties.StringProperty()

        val = prop.deflate("xpto")
        self.assertTrue(val == "xpto")

        val = prop.deflate(None)
        self.assertTrue(val is None)

    def test_should_inflate_choice_string(self):
        prop = properties.StringProperty(choices=["a","b"])

        val = prop.inflate("b")
        self.assertTrue(val == "b")
        val = prop.inflate("a")
        self.assertTrue(val == "a")

        self.assertRaises(ValueError, prop.inflate, None)
        self.assertRaises(ValueError, prop.inflate, 'c')

    def test_should_inflate_choice_map(self):
        prop = properties.StringProperty(choices={"a":'1', "b":'2'})

        val = prop.inflate("b")
        self.assertTrue(val == "2")
        val = prop.inflate("a")
        self.assertTrue(val == "1")

        self.assertRaises(ValueError, prop.inflate, None)
        self.assertRaises(ValueError, prop.inflate, 'c')

    def test_should_inflate_default(self):
        prop = properties.StringProperty(default="33")
        val = prop.inflate(None)
        self.assertTrue(val == "33")
        prop = properties.StringProperty(default=lambda: 22)
        val = prop.inflate(None)
        self.assertTrue(val == '22')

    def test_should_inflate_normalized_string(self):
        prop = properties.StringProperty(norm_func=lambda x:str(x).upper())
        val = prop.inflate("test_norm_string")
        self.assertTrue(val == "TEST_NORM_STRING")

    def test_should_deflate_choice_string(self):
        prop = properties.StringProperty(choices=["a", "b"])

        val = prop.deflate("b")
        self.assertTrue(val == "b")
        val = prop.deflate("a")
        self.assertTrue(val == "a")

        self.assertRaises(ValueError, prop.deflate, None)
        self.assertRaises(ValueError, prop.deflate, 'c')

    def test_should_deflate_the_reveted_choice_map_value(self):
        prop = properties.StringProperty(choices={"a": '1', "b": '2'}, should_revert=True)

        val = prop.deflate("2")
        self.assertTrue(val == "b")
        val = prop.deflate("1")
        self.assertTrue(val == "a")

        self.assertRaises(ValueError, prop.deflate, None)
        self.assertRaises(ValueError, prop.deflate, 'c')

    def test_should_deflate_choice_map_property_raw_value(self):
        prop = properties.StringProperty(choices={"a": '1', "b": '2'})

        val = prop.deflate("2")
        self.assertTrue(val == "2")
        val = prop.deflate("1")
        self.assertTrue(val == "1")

        self.assertRaises(ValueError, prop.deflate, None)
        self.assertRaises(ValueError, prop.deflate, 'c')

    def test_should_deflate_default(self):
        prop = properties.StringProperty(default="33")
        val = prop.deflate(None)
        self.assertTrue(val == "33")
        prop = properties.StringProperty(default=lambda: 22)
        val = prop.deflate(None)
        self.assertTrue(val == 22)

    def test_should_deflate_uft8(self):
        prop = properties.StringProperty()
        value = "informações"
        ret = prop.deflate(value)
        self.assertTrue(value == ret)


class IntegerPropertyTests(unittest.TestCase):

    def test_should_inflate_int(self):
        prop = properties.IntegerProperty()
        value = prop.inflate(1)
        self.assertTrue((value == 1))

        value = prop.inflate('1')
        self.assertTrue(value == 1)
        self.assertTrue(prop.inflate(None) is None)
        self.assertRaises(ValueError, prop.deflate, 'c')

    def test_should_deflate_int(self):
        prop = properties.IntegerProperty()
        value = prop.deflate(1)
        self.assertTrue((value == 1))

        value = prop.deflate('1')
        self.assertTrue(value == 1)

        self.assertRaises(ValueError, prop.deflate, 'c')


class FloatPropertyTests(unittest.TestCase):

    def test_should_inflate(self):
        prop = properties.FloatProperty()
        value = prop.inflate(1.2)
        self.assertTrue((value == 1.2))

        value = prop.inflate('1.2')
        self.assertTrue(value == 1.2)
        self.assertTrue(prop.inflate(None) is None)

        self.assertRaises(ValueError, prop.deflate, 'c')

    def test_should_deflate_int(self):
        prop = properties.FloatProperty()
        value = prop.deflate(1.2)
        self.assertTrue((value == 1.2))

        value = prop.deflate('1.2')
        self.assertTrue(value == 1.2)

        self.assertRaises(ValueError, prop.deflate, 'c')


class BooleanPropertyTests(unittest.TestCase):

    def test_should_inflate(self):
        prop = properties.BooleanProperty()
        value = prop.inflate(True)
        self.assertTrue(value)

        value = prop.inflate('True')
        self.assertTrue(value is True)
        self.assertTrue(prop.inflate('False') is False)

    def test_should_inflate_from_trues_str_list(self):
        prop = properties.BooleanProperty(trues_str_list=['true', '1', 't', 'y', 'yes', 's', 'sim'])
        value = prop.inflate(True)
        self.assertTrue(value)

        value = prop.inflate('True')
        self.assertTrue(value is True)
        self.assertTrue(prop.inflate('False') is False)

    def test_should_deflate_int(self):
        prop = properties.BooleanProperty()
        value = prop.deflate(1.2)
        self.assertTrue(value)

        value = prop.deflate('true')
        self.assertTrue(value)

        # self.assertRaises(ValueError, prop.deflate, 'c')


class DateProperty(unittest.TestCase):

    def test_should_inflate_date(self):
        from datetime import date
        dt = date.today()

        prop = properties.DateProperty()
        val = prop.inflate(dt)
        self.assertTrue(date.today() == val)

    def test_should_inflate_from_str(self):
        from datetime import date
        date_str = '01-12-2017'

        prop = properties.DateProperty(mask='%d-%m-%Y')
        self.assertTrue(date(2017,12, 1) == prop.inflate(date_str))

    def test_should_raise_type_error(self):
        prop = properties.DateProperty(mask='%d-%m-%Y')
        self.assertRaises(TypeError, prop.inflate, 33)

    def test_should_inflate_None(self):
        prop = properties.DateProperty()
        self.assertTrue(None is prop.inflate(None))

    def test_should_deflate_date_to_str(self):
        from datetime import date
        dt = date.today()

        prop = properties.DateProperty()
        val = prop.deflate(dt)
        self.assertTrue(isinstance(val, str))
        self.assertTrue(val == dt.strftime(prop.mask))


class ArrayProperty(unittest.TestCase):

    def test_should_inflate_array_property(self):
        from simple_mappers import MapDefinition
        from simple_mappers import JsonObject

        class TestClass(MapDefinition):
            val1 = properties.StringProperty()
            val2 = properties.StringProperty()

        prop = properties.ArrayProperty(itens_type=TestClass)
        values = [JsonObject(val1="str", val2="str"), JsonObject(val1="str", val2="str")]

        result = prop.inflate(values)
        for r in result:
            self.assertTrue(isinstance(r,TestClass))
            self.assertTrue(r.val1 == "str")
            self.assertTrue(r.val2 == "str")

if __name__ == "__main__":
    unittest.main()