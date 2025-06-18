import unittest
from decimal import Decimal, InvalidOperation
from tabbyset.utils import round_to_tick, floor_to_tick, ceil_to_tick, is_multiple_of_tick


class TestTickUtils(unittest.TestCase):
    def test_is_multiple_of_tick(self):
        with self.subTest(number_type='Decimal'):
            self.assertFalse(is_multiple_of_tick(Decimal('1.2'), Decimal('0.5')))
            self.assertFalse(is_multiple_of_tick(Decimal('1.7'), Decimal('0.5')))
            self.assertTrue(is_multiple_of_tick(Decimal('1.7'), Decimal('0.1')))
            self.assertTrue(is_multiple_of_tick(Decimal('1.7'), Decimal('0')))
        with self.subTest(number_type='float'):
            self.assertFalse(is_multiple_of_tick(1.2, 0.5))
            self.assertFalse(is_multiple_of_tick(1.7, 0.5))
            self.assertTrue(is_multiple_of_tick(1.7, 0.1))
            self.assertTrue(is_multiple_of_tick(1.7, 0))
        with self.subTest(number_type='int'):
            self.assertTrue(is_multiple_of_tick(1, 1))
            self.assertTrue(is_multiple_of_tick(2, 1))
            self.assertTrue(is_multiple_of_tick(2, 0))
        with self.subTest(number_type='str'):
            self.assertFalse(is_multiple_of_tick('1.2', '0.5'))
            self.assertFalse(is_multiple_of_tick('1.7', '0.5'))
            self.assertTrue(is_multiple_of_tick('1.7', '0.1'))
            self.assertTrue(is_multiple_of_tick('1.7', '0'))
        with self.assertRaises(InvalidOperation):
            is_multiple_of_tick('1.7', 'a')

    def test_floor_to_tick(self):
        with self.subTest(number_type='Decimal'):
            self.assertEqual(floor_to_tick(Decimal('1.2'), Decimal('0.5')), Decimal('1'))
            self.assertEqual(floor_to_tick(Decimal('1.7'), Decimal('0.5')), Decimal('1.5'))
            self.assertEqual(floor_to_tick(Decimal('1.7'), Decimal('0.1')), Decimal('1.7'))
            self.assertEqual(floor_to_tick(Decimal('1.7'), Decimal('0')), Decimal('1.7'))
        with self.subTest(number_type='float'):
            self.assertEqual(floor_to_tick(1.2, 0.5), Decimal('1'))
            self.assertEqual(floor_to_tick(1.7, 0.5), Decimal('1.5'))
            self.assertEqual(floor_to_tick(1.7, 0.1), Decimal('1.7'))
            self.assertEqual(floor_to_tick(1.7, 0), Decimal('1.7'))
        with self.subTest(number_type='int'):
            self.assertEqual(floor_to_tick(1, 1), Decimal('1'))
            self.assertEqual(floor_to_tick(2, 1), Decimal('2'))
            self.assertEqual(floor_to_tick(2, 0), Decimal('2'))
        with self.subTest(number_type='str'):
            self.assertEqual(floor_to_tick('1.2', '0.5'), Decimal('1'))
            self.assertEqual(floor_to_tick('1.7', '0.5'), Decimal('1.5'))
            self.assertEqual(floor_to_tick('1.7', '0.1'), Decimal('1.7'))
            self.assertEqual(floor_to_tick('1.7', '0'), Decimal('1.7'))
        with self.assertRaises(InvalidOperation):
            floor_to_tick('1.7', 'a')

    def test_ceil_to_tick(self):
        with self.subTest(number_type='Decimal'):
            self.assertEqual(ceil_to_tick(Decimal('1.2'), Decimal('0.5')), Decimal('1.5'))
            self.assertEqual(ceil_to_tick(Decimal('1.7'), Decimal('0.5')), Decimal('2'))
            self.assertEqual(ceil_to_tick(Decimal('1.7'), Decimal('0.1')), Decimal('1.7'))
            self.assertEqual(ceil_to_tick(Decimal('1.7'), Decimal('0')), Decimal('1.7'))
        with self.subTest(number_type='float'):
            self.assertEqual(ceil_to_tick(1.2, 0.5), Decimal('1.5'))
            self.assertEqual(ceil_to_tick(1.7, 0.5), Decimal('2'))
            self.assertEqual(ceil_to_tick(1.7, 0.1), Decimal('1.7'))
            self.assertEqual(ceil_to_tick(1.7, 0), Decimal('1.7'))
        with self.subTest(number_type='int'):
            self.assertEqual(ceil_to_tick(1, 1), Decimal('1'))
            self.assertEqual(ceil_to_tick(2, 1), Decimal('2'))
            self.assertEqual(ceil_to_tick(2, 0), Decimal('2'))
        with self.subTest(number_type='str'):
            self.assertEqual(ceil_to_tick('1.2', '0.5'), Decimal('1.5'))
            self.assertEqual(ceil_to_tick('1.7', '0.5'), Decimal('2'))
            self.assertEqual(ceil_to_tick('1.7', '0.1'), Decimal('1.7'))
            self.assertEqual(ceil_to_tick('1.7', '0'), Decimal('1.7'))
        with self.assertRaises(InvalidOperation):
            ceil_to_tick('1.7', 'a')

    def test_round_to_tick(self):
        with self.subTest(number_type='Decimal'):
            self.assertEqual(round_to_tick(Decimal('1.2'), Decimal('0.5')), Decimal('1'))
            self.assertEqual(round_to_tick(Decimal('1.8'), Decimal('0.5')), Decimal('2'))
            self.assertEqual(round_to_tick(Decimal('1.7'), Decimal('0.1')), Decimal('1.7'))
            self.assertEqual(round_to_tick(Decimal('1.7'), Decimal('0')), Decimal('1.7'))
        with self.subTest(number_type='float'):
            self.assertEqual(round_to_tick(1.2, 0.5), Decimal('1'))
            self.assertEqual(round_to_tick(1.8, 0.5), Decimal('2'))
            self.assertEqual(round_to_tick(1.7, 0.1), Decimal('1.7'))
            self.assertEqual(round_to_tick(1.7, 0), Decimal('1.7'))
        with self.subTest(number_type='int'):
            self.assertEqual(round_to_tick(1, 1), Decimal('1'))
            self.assertEqual(round_to_tick(2, 1), Decimal('2'))
            self.assertEqual(round_to_tick(2, 0), Decimal('2'))
        with self.subTest(number_type='str'):
            self.assertEqual(round_to_tick('1.2', '0.5'), Decimal('1'))
            self.assertEqual(round_to_tick('1.8', '0.5'), Decimal('2'))
            self.assertEqual(round_to_tick('1.7', '0.1'), Decimal('1.7'))
            self.assertEqual(round_to_tick('1.7', '0'), Decimal('1.7'))
        with self.assertRaises(InvalidOperation):
            round_to_tick('1.7', 'a')
