import unittest
from unittest import mock

from .task1 import predict_message_mood, SomeModel


class TestPredictMessage(unittest.TestCase):
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

    # def test_friends_single(self):

    #     with mock.patch("task1.predict") as mock_api:
    #         mock_api.side_effect = [["voz"], ["voz", "lisa"]]

    #         friends = usr.get_friends()
    #         self.assertEqual(["voz"], friends)

    #         calls = [
    #             mock.call("/friends", "steve", part=None),
    #         ]
    #         self.assertEqual(calls, mock_api.mock_calls)

    #         friends = usr.get_friends("is")
    #         self.assertEqual(["lisa"], friends)

    #         calls = [
    #             mock.call("/friends", "steve", part=None),
    #             mock.call("/friends", "steve", part="IS"),
    #         ]
    #         self.assertEqual(calls, mock_api.mock_calls)

    #         # friends = usr.get_friends("is")

    # @mock.patch("user.fetch_vk_api")
    # def test_friends_no_filter(self, mock_api):
    #     usr = User("steve", 42)

    #     def get_friends(*_, **__):
    #         return ["voz", "lisa"]

    #     mock_api.side_effect = get_friends

    #     friends = usr.get_friends()
    #     self.assertEqual(["voz", "lisa"], friends)

    #     calls = [
    #         mock.call("/friends", "steve", part=None),
    #     ]
    #     self.assertEqual(calls, mock_api.mock_calls)

    #     friends = usr.get_friends()
    #     self.assertEqual(["voz", "lisa"], friends)

    #     calls = [
    #         mock.call("/friends", "steve", part=None),
    #         mock.call("/friends", "steve", part=None),
    #     ]
    #     self.assertEqual(calls, mock_api.mock_calls)

    # @mock.patch("user.fetch_vk_api")
    # def test_friends_connection_error(self, mock_api):
    #     usr = User("steve", 42)

    #     mock_api.side_effect = Exception("connection error")

    #     with self.assertRaises(Exception) as err:
    #         usr.get_friends()

    #     self.assertEqual("connection error", str(err.exception))

    #     calls = [
    #         mock.call("/friends", "steve", part=None),
    #     ]
    #     self.assertEqual(calls, mock_api.mock_calls)

    #     with self.assertRaises(Exception) as err:
    #         usr.get_friends("is")

    #     self.assertEqual("connection error", str(err.exception))

    #     calls = [
    #         mock.call("/friends", "steve", part=None),
    #         mock.call("/friends", "steve", part="IS"),
    #     ]
    #     self.assertEqual(calls, mock_api.mock_calls)
