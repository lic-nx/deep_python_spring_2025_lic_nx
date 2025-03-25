import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from unittest.mock import Mock
from _02.task1 import process_json

class TestProcessJson(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("\nТестированае первого задания второго дня")
    def test_example(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["WORD1", "word2"]

        # Create a mock callback function
        callback = Mock()

        # Call the function with the mock callback
        process_json(json_str, required_keys, tokens, callback)

        # Assert that the callback was called with the expected arguments
        expected_calls = [
            unittest.mock.call("key1", "WORD1"),
            unittest.mock.call("key1", "word2"),
            unittest.mock.call("key2", "word2")
        ]
        callback.assert_has_calls(expected_calls, any_order=True)