from tabbyset.db.id_utils import new_id, is_valid_id, get_id_from_steps
from tabbyset.entities.test_case import TestCase
from tabbyset.testing import TestCaseAssertions

class TestIdUtils(TestCaseAssertions):
    def test_new_id(self):
        id1 = new_id()
        id2 = new_id()
        self.assertNotEqual(id1, id2)

    def test_is_valid_id(self):
        self.assertTrue(is_valid_id(new_id()))
        self.assertTrue(is_valid_id("c5b52f89-d85e-48cc-b749-dd911b1e7526"))
        self.assertFalse(is_valid_id("not a valid id"))

    def test_get_id_from_steps(self):
        pregenerated_id = 'b88ec4b5-23a6-5743-8f3e-1173a82c107e'

        test_case = TestCase(name='TestCase', steps=[
            {'A': 'B', 'C': 'D'},
            {'E': 'F', 'G': 'H'},
        ])
        id1 = get_id_from_steps(test_case)
        id2 = get_id_from_steps(test_case.copy())
        self.assertEqual(id1, id2, 'The ID should be the same for the same steps')
        self.assertEqual(id1, pregenerated_id, 'The ID should be the same between runs')

        test_case.steps = [
            {'A': 'B', 'C': 'D'},
            {'E': 'F', 'G': 'H', 'I': 'J'},
        ]
        id3 = get_id_from_steps(test_case)
        self.assertNotEqual(id1, id3, 'The ID should be different for different steps')
        self.assertNotEqual(id2, id3, 'The ID should be different for different steps')