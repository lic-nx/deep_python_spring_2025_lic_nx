from unittest import mock
import unittest
import os
import sys
from message_evaluation import predict_message_mood, SomeModel

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestPredictMessageMood(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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
