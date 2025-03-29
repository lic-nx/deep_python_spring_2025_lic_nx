from unittest.mock import mock_open
from unittest import mock
import unittest
import os
import sys
from customList import CustomList
import inspect

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class TestCustomList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nТестированае класса CustomList")
    
    def test_class_is_create(self):
       self.assertEqual(inspect.isclass(CustomList), True)

    def test_class_is_subclass(self):
       self.assertEqual(issubclass (CustomList, list), True)