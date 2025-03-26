import unittest
import os
import sys
from parameterizable_decorator import retry_deco

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TrivialException(Exception):
    def __str__(cls):
        return "Недопустимое значение"


class TestDecoratoirs(unittest.TestCase):
    def test_example(self):
        print("\nТестироване декоратора")

    def test_function_with_args(self):
        @retry_deco(1)
        def function_with_args():
            return 1

        result = function_with_args()
        assert result == 1

    def test_retry_on_exception(self):
        @retry_deco(restarts=1, exceptions=[TrivialException])
        def function_with_args():
            return 1 / 0

        with self.assertRaises(ZeroDivisionError):
            function_with_args()

    def test_retry_on_exception_vith_custom(self):
        def runs_tests():
            start_coint = 0

            @retry_deco(restarts=2, exceptions=[ZeroDivisionError])
            def function_with_args(value: int):
                nonlocal start_coint
                if start_coint < 1:
                    start_coint += 1
                    raise TrivialException()
                return value

            return function_with_args

        function_with_args = runs_tests()
        with self.assertRaises(TrivialException):
            function_with_args(3)

        # Test that the function returns the value when the condition is not met
        result = function_with_args(1)
        self.assertEqual(result, 1)
