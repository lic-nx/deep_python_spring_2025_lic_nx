# pylint: disable=I1101

'''проверка что модуль на си работает'''
import unittest
import custom_json


class TestLoads(unittest.TestCase):
    '''класс с тестами для конвертора строки в словарь '''
    def test_simple_loads(self):
        '''тесты корректной работы'''
        self.assertEqual(
            custom_json.loads('{"first":"first", "second":2}'),
            {"first": "first", "second": 2},
        )
        self.assertEqual(
            custom_json.loads('{"first":1, "second":"second"}'),
            {"first": 1, "second": "second"},
        )
        self.assertEqual(
            custom_json.loads('{"empty":"", "none":0}'),
            {"empty": "", "none": 0}
        )
        self.assertEqual(custom_json.loads("{}"), {})

    def test_errors_loads(self):
        '''передача ошибочных строк '''
        with self.assertRaises(TypeError):
            custom_json.loads('{"hello": 10, "world": value}')
        with self.assertRaises(TypeError):
            custom_json.loads('"hello": 10, "world": "value"}')
        with self.assertRaises(TypeError):
            custom_json.loads('{"hello": 10, "world": "value"')
        with self.assertRaises(TypeError):
            custom_json.loads('{"hello", 10, "world", "value"}')
        with self.assertRaises(TypeError):
            custom_json.loads('{"hello": , "world" : "value"}')


class TestDumps(unittest.TestCase):
    '''тест для конвертора в строку'''
    def test_simple_dumps(self):
        '''проверка работы конвертора с правильными входными данными'''
        self.assertEqual(
            custom_json.dumps({"first": "first", "second": 2}),
            '{"first" : "first", "second" : 2}',
        )
        self.assertEqual(
            custom_json.dumps({"first": 1, "second": "second"}),
            '{"first" : 1, "second" : "second"}',
        )
        self.assertEqual(
            custom_json.dumps({"empty": "", "none": 0}),
            '{"empty" : "", "none" : 0}'
        )
        self.assertEqual(custom_json.dumps({}), "{}")

    def test_errors_loads(self):
        '''проверка ошибочных данных '''
        with self.assertRaises(TypeError):
            custom_json.dumps(["hello", 10, "world"])
