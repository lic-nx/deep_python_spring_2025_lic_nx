import unittest
from unittest import mock

from .'01'.task1 import predict_message_mood, SomeModel
from .'01'.task2 import filtered_file_reader
from unittest.mock import mock_open, patch


class TestFirstTask(unittest.TestCase):
    """Тесты для первого задания первой домашки"""

    @classmethod
    def setUpClass(cls):
        print("\nТесты для первого задания первой домашки")

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
    """Тесты для второго задания первой домашки"""

    @classmethod
    def setUpClass(cls):
        print("\nТесты для второго задания первой домашки")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="роза упала на лапу Азора\nроза цветет\n",
    )
    def test_from_example(self, mock_file):
        find_words = ["роза"]
        stop_words = ["азора"]

        # Преобразуем генератор в список для проверки результатов
        result = list(filtered_file_reader("fake_file.txt", find_words, stop_words))

        # Проверяем, что возвращается только одна строка
        self.assertEqual(result, ["роза цветет"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
