from unittest.mock import mock_open, patch, MagicMock
from unittest import mock
import unittest
import os
import sys
from generator_for_reading_filtering_file import filtered_file_reader

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestFilteredFileReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nТестированае генератора")

    @mock.patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="роза упала на лапу Азора\nроза цветет\n",
    )
    def test_from_example(self, mock_file):
        find_words = ["роза"]
        stop_words = ["азора"]
        with mock.patch("builtins.open", mock_file):
            result = list(filtered_file_reader("mock_file",
                                               find_words, stop_words))
            self.assertEqual(result, ["роза цветет"])

    @mock.patch(
        "builtins.open",
        new_callable=mock.mock_open,
        read_data="",
    )
    def test_empty(self, mock_file):
        find_words = ["роза"]
        stop_words = ["азора"]
        with mock.patch("builtins.open", mock_file):
            result = list(filtered_file_reader("mock_file",
                                               find_words, stop_words))
            self.assertEqual(result, [])

    @mock.patch(
        "builtins.open",
        new_callable=mock.mock_open,
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
    def test_alot_find_words_with_filename(self, mock_file):
        find_words = ["нам", "а", "взгляд"]
        stop_words = ["азора"]
        with mock.patch("builtins.open", mock_file):
            result = list(filtered_file_reader("mock_file",
                                               find_words, stop_words))
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
        with mock.patch("builtins.open", mock_file):
            result = list(filtered_file_reader("mock_file",
                                               find_words, stop_words))
            self.assertEqual(
                result,
                [],
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
    def test_str_in_stop(self, mock_file):
        find_words = ["нам", "иного",
                      "выбора кроме определения модели развития"]
        stop_words = ["нам иного выбора кроме определения модели развития"]
        with mock.patch("builtins.open", mock_file):
            result = list(filtered_file_reader("mock_file",
                                               find_words, stop_words))
            self.assertEqual(
                result,
                [],
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
    def test_full_str_in_stop(self, mock_file):
        find_words = [
            "нам иного выбора кроме определения модели развития ",
            "открывает новые горизонты для стандартных подходов",
        ]
        stop_words = ["открывает новые горизонты для стандартных подходов"]
        with mock.patch("builtins.open", mock_file):
            result = list(filtered_file_reader("mock_file",
                                               find_words, stop_words))
            self.assertEqual(
                result,
                [
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
    def test_check_cchars(self, mock_file):
        find_words = ["а", "с"]
        stop_words = ["д", "в"]
        with mock.patch("builtins.open", mock_file):
            result = list(filtered_file_reader("mock_file",
                                               find_words, stop_words))
            self.assertEqual(
                result,
                [
                    "С учётом сложившейся международной обстановки",
                    "а также свежий взгляд на привычные вещи безусловно",
                ],
            )

    @mock.patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="с УчЁТоМ слОжИвШеЙсЯ мЕжДуНарОдНоЙ оБсТаНоВкИ \
            \nНоВаЯ мОдЕлЬ орГаНиЗаЦиОнНоЙ дЕяТеЛьНоСтИ \
            \nА тАкЖе СвЕжИй ВзГлЯд нА пРиВыЧнЫе ВеЩи бЕзУсЛоВнО \
            \nОтКрЫвАеТ нОвЫе ГорИзОнТы ДлЯ сТаНдАрТнЫх пОдХоДоВ \
            \nуЧиТыВаЯ кЛюЧеВыЕ сЦеНаРиИ пОвЕдЕнИя пЕрСпЕкТиВнОе \
            \nПлАнИрОвАнИе ОдНоЗнАчНо фИкСиРуЕт нЕоБхОдИмОсТь \
            \nНаПрАвЛеНиЙ пРоГрЕсСиВнОгО рАзВиТиЯ БеЗуСлОвНо \
            \nЭкОнОмИчЕсКаЯ пОвЕсТкА сЕгОдНяШнЕгО дНя НЕ дАёТ \
            \nНАм ИнОгО вЫбОрА кРоМе ОпРеДеЛеНиЯ мОдЕлИ рАзВиТиЯ",
    )
    def test_check_register(self, mock_file):
        find_words = ["а", "с"]
        stop_words = ["д", "в"]
        with mock.patch("builtins.open", mock_file):
            result = list(filtered_file_reader("mock_file",
                                               find_words, stop_words))
            self.assertEqual(
                result,
                [
                    "с УчЁТоМ слОжИвШеЙсЯ мЕжДуНарОдНоЙ оБсТаНоВкИ",
                    "А тАкЖе СвЕжИй ВзГлЯд нА пРиВыЧнЫе ВеЩи бЕзУсЛоВнО",
                ],
            )

    @mock.patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="с УчЁТоМ слОжИвШеЙсЯ мЕжДуНарОдНоЙ оБсТаНоВкИ \
            \nНоВаЯ мОдЕлЬ орГаНиЗаЦиОнНоЙ дЕяТеЛьНоСтИ \
            \nА тАкЖе СвЕжИй ВзГлЯд нА пРиВыЧнЫе ВеЩи бЕзУсЛоВнО \
            \nОтКрЫвАеТ нОвЫе ГорИзОнТы ДлЯ сТаНдАрТнЫх пОдХоДоВ \
            \nуЧиТыВаЯ кЛюЧеВыЕ сЦеНаРиИ пОвЕдЕнИя пЕрСпЕкТиВнОе \
            \nПлАнИрОвАнИе ОдНоЗнАчНо фИкСиРуЕт нЕоБхОдИмОсТь \
            \nНаПрАвЛеНиЙ пРоГрЕсСиВнОгО рАзВиТиЯ БеЗуСлОвНо \
            \nЭкОнОмИчЕсКаЯ пОвЕсТкА сЕгОдНяШнЕгО дНя НЕ дАёТ \
            \nНАм ИнОгО вЫбОрА кРоМе ОпРеДеЛеНиЯ мОдЕлИ рАзВиТиЯ",
    )
    def test_check_2_register(self, mock_file):
        find_words = ["нАм", "с"]
        stop_words = ["повестка", "КЛЮЧЕВЫЕ"]
        with mock.patch("builtins.open", mock_file):
            result = list(filtered_file_reader("mock_file",
                                               find_words, stop_words))
            self.assertEqual(
                result,
                [
                    "с УчЁТоМ слОжИвШеЙсЯ мЕжДуНарОдНоЙ оБсТаНоВкИ",
                    "НАм ИнОгО вЫбОрА кРоМе ОпРеДеЛеНиЯ мОдЕлИ рАзВиТиЯ",
                ],
            )

    def test_filename_valid(self):
        mock_file_content = "hello world\nfiltered text\nstop words here"
        find_words = ["filtered"]
        stop_words = ["stop"]

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = list(filtered_file_reader("test_file.txt",
                                               find_words, stop_words))
            self.assertEqual(result, ["filtered text"])

    def test_file_object_valid(self):
        mock_file = MagicMock()
        mock_file.__iter__.return_value = iter(
            ["hello world\n", "filtered text\n", "stop words here\n"]
        )
        find_words = ["filtered"]
        stop_words = ["stop"]

        result = list(filtered_file_reader(mock_file, find_words, stop_words))
        self.assertEqual(result, ["filtered text"])

    def test_empty_file(self):
        mock_file_content = ""
        find_words = ["filtered"]
        stop_words = ["stop"]

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = list(filtered_file_reader("test_file.txt",
                                               find_words, stop_words))
            self.assertEqual(result, [])

    def test_no_matches(self):
        mock_file_content = "no matches here\nanother line without matches"
        find_words = ["filtered"]
        stop_words = ["stop"]

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = list(filtered_file_reader("test_file.txt",
                                               find_words, stop_words))
            self.assertEqual(result, [])

    def test_invalid_argument(self):
        find_words = ["filtered"]
        stop_words = ["stop"]

        with self.assertRaises(ValueError):
            list(filtered_file_reader(12345, find_words, stop_words))
