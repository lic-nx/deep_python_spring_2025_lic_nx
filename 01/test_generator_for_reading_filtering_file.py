from unittest.mock import mock_open
from unittest import mock
import unittest
import os
import sys
from generator_for_reading_filtering_file import filtered_file_reader

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestFilteredFileReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nТестированае ггениратора")

    @mock.patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="роза упала на лапу Азора\nроза цветет\n",
    )
    def test_from_example(self, mock_file):
        find_words = ["роза"]
        stop_words = ["азора"]

        # Преобразуем генератор в список для проверки результатов
        result = list(filtered_file_reader(mock_file, find_words, stop_words))

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

        result = list(filtered_file_reader(mock_file, find_words, stop_words))

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
        result = list(filtered_file_reader(mock_file, find_words, stop_words))

        # Проверяем, что возвращается только одна строка
        self.assertEqual(
            result,
            [
                "а также свежий взгляд на привычные вещи безусловно",
                "нам иного выбора кроме определения модели развития",
            ],
        )

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
    def test_empty_find_words(self, mock_file):
        find_words = []
        stop_words = ["азора"]

        # Преобразуем генератор в список для проверки результатов
        result = list(filtered_file_reader(mock_file, find_words, stop_words))

        # Проверяем, что возвращается только одна строка
        self.assertEqual(
            result,
            [],
        )
