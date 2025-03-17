import unittest
from unittest import mock
from _01.task1 import predict_message_mood, SomeModel
from _01.task2 import filtered_file_reader
from unittest.mock import mock_open


class TestFirstTask(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("\nТестированае первого задания первого дня")

    def test_from_example(self):
        with mock.patch.object(SomeModel, "predict") as mock_api:
            mock_api.side_effect = [0.9, 0.9, 0.2]

            self.assertEqual("отл", predict_message_mood("Чапаев и пустота"))
            self.assertEqual(
                "норм", predict_message_mood("Чапаев и пустота", 0.8, 0.99)
            )
            self.assertEqual("неуд", predict_message_mood("Вулкан"))

    def test_vrong_params(self):
        with mock.patch.object(SomeModel, "predict") as mock_api:
            mock_api.return_value = 1.2

            # Проверка выброса ValueError с сообщением "value err"
            with self.assertRaises(ValueError) as cm:
                predict_message_mood("Чапаев и пустота")
            self.assertEqual(str(cm.exception), "value err")

            # Проверка выброса ValueError с сообщением "Err"
            with self.assertRaises(ValueError) as cm:
                predict_message_mood("Чапаев и пустота", -1)
            self.assertEqual(str(cm.exception), "Err")

            with self.assertRaises(ValueError) as cm:
                predict_message_mood("Чапаев и пустота", 0.6, 0.2)
            self.assertEqual(str(cm.exception), "Err")

            with self.assertRaises(ValueError) as cm:
                predict_message_mood("Чапаев и пустота", 0.6, 1.2)
            self.assertEqual(str(cm.exception), "Err")


class TestSecondTask(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("\nТестированае второго задания первого дня")


    @mock.patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="роза упала на лапу Азора\nроза цветет\n",
    )
    def test_from_example(self, mock_file):
        find_words = ["роза"]
        stop_words = ["азора"]

        # Преобразуем генератор в список для проверки результатов
        result = list(filtered_file_reader("f_f.txt", find_words, stop_words))

        # Проверяем, что возвращается только одна строка
        self.assertEqual(result, ["роза цветет"])

    @mock.patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="",
    )

    def test_empty(self, mock_file):
        find_words = ["роза"]
        stop_words = ["азора"]
        # Преобразуем генератор в список для проверки результатов
        result = list(filtered_file_reader("file.txt", find_words, stop_words))
        # Проверяем, что возвращается только одна строка
        self.assertEqual(result, [])


    @mock.patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="С учётом сложившейся международной обстановки \
            \nновая модель организационной деятельности \
            \nа также свежий взгляд на привычные вещи безусловно \
            \nоткрывает новые горизонты для стандартных подходов \
            \nУчитывая ключевые сценарии поведения перспективное \
            \nпланирование однозначно фиксирует необходимость \
            \nнаправлений прогрессивного развития \nБезусловно \
            \nэкономическая повестка сегодняшнего дня не даёт \
            \nнам иного выбора кроме определения модели развития",
    )
    def test_alot_find_words(self, mock_file):
        find_words = ["нам", "а", "взгляд"]
        stop_words = ["азора"]

        # Преобразуем генератор в список для проверки результатов
        result = list(filtered_file_reader("file.txt", find_words, stop_words))

        # Проверяем, что возвращается только одна строка
        self.assertEqual(
            result,
            [
                "а также свежий взгляд на привычные вещи безусловно",
                "нам иного выбора кроме определения модели развития",
            ],
        )
