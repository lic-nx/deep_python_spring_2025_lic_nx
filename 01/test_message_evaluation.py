from unittest import mock
import unittest
import os
import sys
from message_evaluation import predict_message_mood, SomeModel

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestPredictMessageMood(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nТестированае строки")

    def test_from_example(self):
        with mock.patch.object(SomeModel, "predict") as mock_api:
            mock_api.side_effect = [0.9, 0.9, 0.2]
            str_for_send = "Чапаев и пустота"
            self.assertEqual("отл", predict_message_mood(str_for_send))
            self.assertEqual("норм",
                             predict_message_mood(str_for_send, 0.8, 0.99))
            mock_api.assert_called_with(str_for_send)
            self.assertEqual("неуд", predict_message_mood("Вулкан"))
            mock_api.assert_called_with("Вулкан")

    def test_vrong_params(self):
        with mock.patch.object(SomeModel, "predict") as mock_api:
            mock_api.return_value = 1.2
            with self.assertRaises(ValueError) as cm:
                predict_message_mood("Чапаев и пустота")
                mock_api.assert_called_with("Чапаев и пустота")
            self.assertEqual(str(cm.exception), "value err")
            with self.assertRaises(ValueError) as cm:
                predict_message_mood("Чапаев и пустота", -1)
                mock_api.assert_called_with("Чапаев и пустота")
            self.assertEqual(str(cm.exception), "Err")

            with self.assertRaises(ValueError) as cm:
                predict_message_mood("Чапаев и пустота", 0.6, 0.2)
                mock_api.assert_called_with("Чапаев и пустота")
            self.assertEqual(str(cm.exception), "Err")

            with self.assertRaises(ValueError) as cm:
                predict_message_mood("Чапаев и пустота", 0.6, 1.2)
                mock_api.assert_called_with("Чапаев и пустота")
            self.assertEqual(str(cm.exception), "Err")

    def test_boundary_conditions(self):
        with mock.patch.object(SomeModel, "predict") as mock_api:
            mock_api.side_effect = [
                0.8,
                1.0,
                0.0,
                0.299999,
                0.3,
                0.799999,
                0.8,
                0.800001,
                0.300001,
            ]
            self.assertEqual("норм", predict_message_mood("0.8"))
            self.assertEqual("отл", predict_message_mood("1.0"))
            self.assertEqual("неуд", predict_message_mood("0.0"))
            self.assertEqual("неуд", predict_message_mood("0.299999"))
            self.assertEqual("норм", predict_message_mood("0.3"))
            self.assertEqual("норм", predict_message_mood("0.799999"))
            self.assertEqual("норм", predict_message_mood("0.8", 0.3, 0.8))
            self.assertEqual("отл", predict_message_mood("0.800001", 0.3, 0.8))
            self.assertEqual("норм", predict_message_mood("0.300001", 0.3, 0.8))
            mock_api.assert_any_call("0.8")
            mock_api.assert_any_call("1.0")
            mock_api.assert_any_call("0.0")
            mock_api.assert_any_call("0.299999")
            mock_api.assert_any_call("0.3")
            mock_api.assert_any_call("0.799999")
            mock_api.assert_any_call("0.8")
            mock_api.assert_any_call("0.800001")
            mock_api.assert_any_call("0.300001")
