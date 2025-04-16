import sys
import os
import unittest
from unittest.mock import Mock
from processing_json import process_json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

tokens = ["WORD1", "word2", "mArkup", "SGML", "SGML1", "", "Markup", "sgml"]


class TestProcessJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nТестированае парсинга строки")

    def test_example(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        expected_calls = [
                            unittest.mock.call("key1", "WORD1"),
                            unittest.mock.call("key1", "word2"),
                            unittest.mock.call("key2", "word2"),
                        ]
        callback.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(callback.call_count, len(expected_calls),
                         "Обнаружены дополнительные вызовы callback!")

    def test_empty_input(self):
        json_str = ""
        required_keys = []
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        self.assertEqual(callback.call_count, 0,
                         "Обнаружены дополнительные вызовы callback!")
    def test_empty_tokens(self):
        json_str = """{"ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986"}"""
        required_keys = []
        callback = Mock()
        tokens = []
        process_json(json_str, required_keys, tokens, callback)
        callback.assert_not_called()
        self.assertEqual(callback.call_count, 0,
                         "Обнаружены дополнительные вызовы callback!")

    def test_empty_keys(self):
        json_str = """{"ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986"}"""
        required_keys = []
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        callback.assert_not_called()
        self.assertEqual(callback.call_count, 0,
                         "Обнаружены дополнительные вызовы callback!")

    def test_missing_required_key(self):
        # Define a sample JSON string
        json_str = """{"ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986"}"""
        required_keys = ["key3"]
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        callback.assert_not_called()
        self.assertEqual(callback.call_count, 0,
                         "Обнаружены дополнительные вызовы callback!")

    def test_missing_tokens_key(self):
        # Define a sample JSON string
        json_str = """{"ID": "SGML_noe",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986"}"""
        required_keys = ["ID"]
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        callback.assert_not_called()
        self.assertEqual(callback.call_count, 0,
                         "Обнаружены дополнительные вызовы callback!")
    def test_dublicates_keys(self):
        # Define a sample JSON string
        json_str = """{"ID": "SGML_noe WORD1",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986"}"""
        required_keys = ["ID", "ID", "id"]
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        callback.assert_not_called()
        self.assertEqual(callback.call_count, 0,
                         "Обнаружены дополнительные вызовы callback!")

    def test_missing_tokens(self):
        json_str = """{"ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986"}"""
        required_keys = ["ID"]
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        expected_calls = [
            unittest.mock.call("ID", "SGML"),
            unittest.mock.call("ID", "sgml")
        ]
        callback.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(callback.call_count, len(expected_calls),
                         "Обнаружены дополнительные вызовы callback!")

    def test_empty_tokens(self):
        json_str = """{"ID": "SGML SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986"}"""
        required_keys = ["ID"]
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        expected_calls = [
            unittest.mock.call("ID", "SGML"),
            unittest.mock.call("ID", "SGML"),
            unittest.mock.call("ID", "sgml"),
            unittest.mock.call('ID', 'sgml')
        ]
        callback.assert_has_calls(expected_calls, any_order=True)
        print("Фактические вызовы:", callback.mock_calls)
        self.assertEqual(callback.call_count, len(expected_calls),
                         "Обнаружены дополнительные вызовы callback!")
        # callback.assert_not_called()

    def test_registers(self):
        json_str = """{"ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986"}"""
        required_keys = ["ID", "SortAs", "glossterm"]
        callback = Mock()
        process_json(json_str, required_keys, tokens, callback)
        expected_calls = [
            unittest.mock.call("ID", "SGML"),
            unittest.mock.call("ID", "sgml"),
            unittest.mock.call("SortAs", "SGML"),
            unittest.mock.call("SortAs", "sgml"),
        ]
        callback.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(callback.call_count, len(expected_calls),
                         "Обнаружены дополнительные вызовы callback!")
