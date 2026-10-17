"""Unit tests for the controller. Run: python -m unittest discover -s tests -t ."""
import unittest

from controller import CommandController
from model import PIMCollection


class TestController(unittest.TestCase):
    def test_supplied_empty_collection_is_kept(self):
        # GAP-05: an empty collection passed in is used, not replaced.
        c = PIMCollection()
        controller = CommandController(c)
        self.assertIs(controller.collection, c)
        controller.execute('create note "hi"')
        self.assertEqual(len(c), 1)


if __name__ == "__main__":
    unittest.main()
