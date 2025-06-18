import unittest
from decimal import Decimal
from tabbyset.utils.flex_table.table_queries import (
    Equal, NotEqual, GreaterThan, GreaterThanOrEqual, LessThan, LessThanOrEqual,
    parse_query_statement, parse_dict_query, apply_query_to_dict
)


class TestTableQueries(unittest.TestCase):

    def test_equal_applies_correctly(self):
        self.assertTrue(Equal(5).apply(5))
        self.assertFalse(Equal(5).apply(4))

    def test_not_equal_applies_correctly(self):
        self.assertTrue(NotEqual(5).apply(4))
        self.assertFalse(NotEqual(5).apply(5))

    def test_greater_than_applies_correctly(self):
        self.assertTrue(GreaterThan(5).apply(6))
        self.assertFalse(GreaterThan(5).apply(5))
        self.assertFalse(GreaterThan(5).apply(4))

    def test_greater_than_or_equal_applies_correctly(self):
        self.assertTrue(GreaterThanOrEqual(5).apply(5))
        self.assertTrue(GreaterThanOrEqual(5).apply(6))
        self.assertFalse(GreaterThanOrEqual(5).apply(4))

    def test_less_than_applies_correctly(self):
        self.assertTrue(LessThan(5).apply(4))
        self.assertFalse(LessThan(5).apply(5))
        self.assertFalse(LessThan(5).apply(6))

    def test_less_than_or_equal_applies_correctly(self):
        self.assertTrue(LessThanOrEqual(5).apply(5))
        self.assertTrue(LessThanOrEqual(5).apply(4))
        self.assertFalse(LessThanOrEqual(5).apply(6))

    def test_parse_query_statement_parses_correctly(self):
        with self.subTest('QueryStatement instance must be preserved'):
            self.assertIsInstance(parse_query_statement(Equal(5)), Equal)
        with self.subTest('"= " at the start must be Equal query'):
            self.assertIsInstance(parse_query_statement('= 5'), Equal)
        with self.subTest('"!= " at the start must be NotEqual query'):
            self.assertIsInstance(parse_query_statement('!= 5'), NotEqual)
        with self.subTest('"> " at the start must be GreaterThan query'):
            self.assertIsInstance(parse_query_statement('> 5'), GreaterThan)
        with self.subTest('">= " at the start must be GreaterThanOrEqual query'):
            self.assertIsInstance(parse_query_statement('>= 5'), GreaterThanOrEqual)
        with self.subTest('"< " at the start must be LessThan query'):
            self.assertIsInstance(parse_query_statement('< 5'), LessThan)
        with self.subTest('"<= " at the start must be LessThanOrEqual query'):
            self.assertIsInstance(parse_query_statement('<= 5'), LessThanOrEqual)
        with self.subTest('non-query string must be Equal query'):
            self.assertIsInstance(parse_query_statement('5'), Equal)
        with self.subTest('non-string value must be Equal query'):
            self.assertIsInstance(parse_query_statement(5), Equal)
        with self.subTest('QueryStatement instance must be preserved'):
            self.assertIsInstance(parse_query_statement(Equal(1)), Equal)

    def test_parse_dict_query_parses_correctly(self):
        query_dict = {
            'a': '= 5',
            'b': '!= 6',
            'c': '> 7',
            'd': '>= 8',
            'e': '< 9',
            'f': '<= 10',
            'g': '11',
            'h': 1,
            'i': Equal(12)
        }
        parsed = parse_dict_query(query_dict)
        with self.subTest('"= " at the start must be Equal query'):
            self.assertIsInstance(parsed['a'], Equal)
        with self.subTest('"!= " at the start must be NotEqual query'):
            self.assertIsInstance(parsed['b'], NotEqual)
        with self.subTest('"> " at the start must be GreaterThan query'):
            self.assertIsInstance(parsed['c'], GreaterThan)
        with self.subTest('">= " at the start must be GreaterThanOrEqual query'):
            self.assertIsInstance(parsed['d'], GreaterThanOrEqual)
        with self.subTest('"< " at the start must be LessThan query'):
            self.assertIsInstance(parsed['e'], LessThan)
        with self.subTest('"<= " at the start must be LessThanOrEqual query'):
            self.assertIsInstance(parsed['f'], LessThanOrEqual)
        with self.subTest('non-query string must be Equal query'):
            self.assertIsInstance(parsed['g'], Equal)
        with self.subTest('non-string value must be Equal query'):
            self.assertIsInstance(parsed['h'], Equal)
        with self.subTest('QueryStatement instance must be preserved'):
            self.assertIsInstance(parsed['i'], Equal)

    def test_apply_query_to_dict_applies_correctly(self):
        query_dict = parse_dict_query({'a': '= 5', 'b': '!= 6'})
        value_dict = {'a': 5, 'b': 7}
        self.assertTrue(apply_query_to_dict(query_dict, value_dict))
        value_dict = {'a': 5, 'b': 6}
        self.assertFalse(apply_query_to_dict(query_dict, value_dict))

    def test_try_number_cast_handles_non_numeric(self):
        self.assertEqual(Equal('abc')._try_number_cast('abc'), 'abc')
        self.assertEqual(Equal('5')._try_number_cast('5'), Decimal('5'))


if __name__ == '__main__':
    unittest.main()
