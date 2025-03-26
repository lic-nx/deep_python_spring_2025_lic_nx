import unittest
import os
import sys
from parameterizable_decorator import retry_deco

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestDecoratoirs(unittest.TestCase):
    def test_example(self):
        print("\nТестироване второго задания второго дня")

    def test_function_with_args(self):
        @retry_deco(1)
        def function_with_args():
            return 1

        result = function_with_args()
        assert result == 1

    def test_retry_on_exception(self):
        @retry_deco(restarts=1, exceptions=[ZeroDivisionError])
        def function_with_args():
            return 1 / 0

        with self.assertRaises(ZeroDivisionError):
            function_with_args()
