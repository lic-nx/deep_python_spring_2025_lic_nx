import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from unittest.mock import Mock
from _02.task1 import process_json
from _02.task2 import retry_deco
class TestProcessJson(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("\nТестированае первого задания второго дня")

    def test_example(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["WORD1", "word2"]
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        expected_calls = [
            unittest.mock.call("key1", "WORD1"),
            unittest.mock.call("key1", "word2"),
            unittest.mock.call("key2", "word2")
        ]
        callback.assert_has_calls(expected_calls, any_order=True)

    def test_empty_input(self):
        json_str = ''
        required_keys = []
        tokens = []
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        callback.assert_not_called()


    def test_empty_keys(self):
        json_str = """{"ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986"}"""
        required_keys = []
        tokens = ["mArkup"]
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        callback.assert_not_called()

    def test_missing_required_key(self):
        # Define a sample JSON string
        json_str = """{"ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986"}"""
        required_keys = ["key3"]
        tokens = ["SGML"]

        # Create a mock callback function
        callback = Mock()

        # Call the function
        process_json(json_str, required_keys, tokens, callback)

        # Assert that the callback was not called
        callback.assert_not_called()
    
    def test_missing_tokens(self):
        # Define a sample JSON string
        json_str = """{"ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986"}"""
        required_keys = ["ID"]
        tokens = ["SGML1"]

        # Create a mock callback function
        callback = Mock()

        # Call the function
        process_json(json_str, required_keys, tokens, callback)

        # Assert that the callback was not called
        callback.assert_not_called()
    
    def test_empty_tokens(self):
        # Define a sample JSON string
        json_str = """{"ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986"}"""
        required_keys = ["ID"]
        tokens = []

        # Create a mock callback function
        callback = Mock()

        # Call the function
        process_json(json_str, required_keys, tokens, callback)

        # Assert that the callback was not called
        callback.assert_not_called()
    def test_registers(self):
        # Define a sample JSON string
        json_str = """{"ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986"}"""
        required_keys = ["ID", "SortAs", "glossterm"]
        tokens = ["Markup", "sgml"]

        # Create a mock callback function
        callback = Mock()

        # Call the function
        process_json(json_str, required_keys, tokens, callback)

        # Assert that the callback was not called
        expected_calls =[
            unittest.mock.call("ID", "sgml"),
            unittest.mock.call("SortAs", "sgml")
        ]
        callback.assert_has_calls(expected_calls, any_order=True)




class TestDecoratoirs(unittest.TestCase):
    def test_example(self):
        print("\nТестироване второго задания второго дня")

    def test_function_with_args(self):
        @retry_deco(1)
        def function_with_args():
            return 1
        result = function_with_args()
        assert result == 1

    def test_retry_on_exception(self):
        @retry_deco(restarts=1, exceptions=[ZeroDivisionError])
        def function_with_args():
            return 1 / 0

        with self.assertRaises(ZeroDivisionError):
            function_with_args()