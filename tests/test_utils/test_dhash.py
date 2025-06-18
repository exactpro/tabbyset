import tabbyset as tbs
import copy
import unittest

class TestDeterministicHash(unittest.TestCase):
    def test_dhash(self):
        for hashable in (1, 'a', (1, 2), [1, 2], {'a': 1}):
            with self.subTest(data_type=type(hashable)):
                hash1 = tbs.dhash(hashable)
                hash2 = tbs.dhash(copy.deepcopy(hashable))
                self.assertEqual(hash1, hash2)