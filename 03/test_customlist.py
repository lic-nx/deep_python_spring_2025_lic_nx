import unittest
import os
import sys
import inspect
from customlist import CustomList


sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def is_equal(left, right):
    if len(left) != len(right):
        return False
    for i, b in zip(left, right):
        if i != b:
            return False
    return True


class TestCustomList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nТестированае класса CustomList")

    def test_class_is_create(self):
        self.assertTrue(inspect.isclass(CustomList), True)

    def test_class_is_subclass(self):
        self.assertTrue(issubclass(CustomList, list), True)

    def test_from_exsample(self):
        self.assertTrue(
            is_equal(
                CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]),
                CustomList([6, 3, 10, 7]),
            )
        )
        self.assertTrue(
            is_equal(
                CustomList([10]) + [2, 5],
                CustomList([12, 5])
                )
            )
        self.assertTrue(
            is_equal(
                [2, 5] + CustomList([10]),
                CustomList([12, 5])
                )
            )
        self.assertTrue(
            is_equal(
                CustomList([2, 5]) + 10,
                CustomList([12, 15])
                )
            )
        self.assertTrue(
            is_equal(
                10 + CustomList([2, 5]),
                CustomList([12, 15])
            )
        )
        self.assertTrue(
            is_equal(
                CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7]),
                CustomList([4, -1, -4, 7])
            )
        )
        self.assertTrue(
            is_equal(
                CustomList([10]) - [2, 5],
                CustomList([8, -5])
            )
        )
        self.assertTrue(
            is_equal(
                [2, 5] - CustomList([10]),
                CustomList([-8, 5])
            )
        )
        self.assertTrue(
            is_equal(
                CustomList([2, 5]) - 10,
                CustomList([-8, -5])
            )
        )
        self.assertTrue(
            is_equal(
                10 - CustomList([2, 5]),
                CustomList([8, 5])
            )
        )

    def test_class_like_list(self):
        cl = CustomList()
        cl.append(4)
        cl.append(5)
        self.assertTrue(is_equal(cl, [4, 5]))
        self.assertIsInstance(cl, CustomList)

    def test_equao(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 4, 3])
        self.assertTrue(cl == other_cl)
        cl.append(5)
        self.assertTrue(cl != other_cl)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)

    def test_greate_then(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 4, 5])
        self.assertFalse(cl > other_cl)
        cl.append(5)
        self.assertTrue(cl > other_cl)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)

    def test_less_then(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 4, 5])
        self.assertTrue(cl < other_cl)
        cl.append(5)
        self.assertFalse(cl < other_cl)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)

    def test_greate_egual_then(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 4, 3])
        self.assertTrue(cl >= other_cl)
        cl.append(5)
        self.assertTrue(cl >= other_cl)


class TestCustomList_2(unittest.TestCase):
    def test_less_egual_then(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 3, 4])
        self.assertTrue(cl <= other_cl)
        cl.append(5)
        self.assertFalse(cl <= other_cl)

    def test_str(self):
        cl = CustomList([1, 2, 3, 4])
        self.assertTrue(str(cl), "CustomList([1, 2, 3, 4]), Sum: 10")

    def test_rsub(self):
        cl = CustomList([1, 2, 4])
        res = 2 - cl
        self.assertTrue(
            is_equal(
                res,
                CustomList([1, 0, -2])
                )
            )
        self.assertTrue(isinstance(res, CustomList))
        other_cl = [1, 1, 1, 1, 1, 1, 1]
        res = other_cl - cl
        self.assertTrue(res, [0, -1, -3, 1, 1, 1, 1])

    def test_rsumm(self):
        cl = CustomList([1, 2, 4])
        res = 2 + cl
        self.assertTrue(
            is_equal(
                res,
                CustomList([3, 4, 6])
            )
        )
        self.assertTrue(isinstance(res, CustomList))
        other_cl = [1, 1, 1, 1, 1, 1, 1]
        res = other_cl + cl
        self.assertTrue(
            is_equal(
                res,
                [2, 3, 5, 1, 1, 1, 1]
            )
        )
        self.assertTrue(
            is_equal(
                other_cl,
                [1, 1, 1, 1, 1, 1, 1]
            )
        )
        self.assertIsInstance(res, CustomList)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, list)

    def test_cl_longest_summ(self):
        cl = CustomList([1, 2, 4, 5])
        other_cl = [1, 1]
        res = other_cl + cl
        self.assertTrue(
            is_equal(
                res,
                [2, 3, 4, 5]
            )
        )
        self.assertTrue(
            is_equal(
                other_cl,
                [1, 1]
            )
        )
        self.assertIsInstance(res, CustomList)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, list)

    def test_cl_summ(self):
        cl = CustomList([1, 2, 4, 5])
        other_cl = CustomList([1, 1])
        res = other_cl + cl
        self.assertTrue(
            is_equal(
                res,
                [2, 3, 4, 5]
            )
        )
        self.assertTrue(
            is_equal(
                other_cl,
                [1, 1]
            )
        )
        self.assertIsInstance(res, CustomList)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)

    def test_addition_same_size(self):
        a = CustomList([1, 2, 3])
        b = CustomList([4, 5, 6])
        result = a + b
        self.assertTrue(
            is_equal(
                result,
                [5, 7, 9])
                )
        self.assertTrue(
            is_equal(
                a,
                [1, 2, 3]
            )
        )
        self.assertTrue(
            is_equal(
                b,
                [4, 5, 6]
            )
        )

    def test_addition_left_longer(self):
        # Сложение, когда левый список длиннее
        a = CustomList([1, 2, 3, 4])
        b = CustomList([5, 6])
        result = a + b
        self.assertTrue(is_equal(result, [6, 8, 3, 4]))
        self.assertTrue(
            is_equal(
                list(a), [1, 2, 3, 4]
                )
        )
        self.assertTrue(
            is_equal(
                list(b),
                [5, 6]
            )
        )

    def test_addition_right_longer(self):
        # Сложение, когда правый список длиннее
        a = CustomList([1, 2])
        b = CustomList([3, 4, 5, 6])
        result = a + b
        self.assertTrue(
            is_equal(
                result,
                [4, 6, 5, 6]
            )
        )
        self.assertTrue(
            is_equal(
                a,
                [1, 2]
            )
        )
        self.assertTrue(is_equal(b, [3, 4, 5, 6]))

    def test_addition_with_regular_list(self):
        # Сложение с обычным списком
        a = CustomList([1, 2, 3])
        b = [4, 5]
        result = a + b
        self.assertTrue(is_equal(result, [5, 7, 3]))
        self.assertTrue(is_equal(a, [1, 2, 3]))
        self.assertTrue(is_equal(b, [4, 5]))

    def test_raddition_with_regular_list(self):
        # Обратное сложение с обычным списком
        a = [4, 5]
        b = CustomList([1, 2, 3])
        result = a + b
        self.assertTrue(is_equal(result, [5, 7, 3]))
        self.assertTrue(is_equal(a, [4, 5]))
        self.assertTrue(is_equal(b, [1, 2, 3]))

    def test_subtraction_same_size(self):
        # Вычитание двух списков одинакового размера
        a = CustomList([10, 20, 30])
        b = CustomList([1, 2, 3])
        result = a - b
        self.assertTrue(is_equal(result, [9, 18, 27]))
        self.assertTrue(is_equal(a, [10, 20, 30]))
        self.assertTrue(is_equal(b, [1, 2, 3]))

    def test_subtraction_left_longer(self):
        # Вычитание, когда левый список длиннее
        a = CustomList([10, 20, 30, 40])
        b = CustomList([1, 2])
        result = a - b
        self.assertTrue(is_equal(result, [9, 18, 30, 40]))
        self.assertTrue(is_equal(a, [10, 20, 30, 40]))
        self.assertTrue(is_equal(b, [1, 2]))

    def test_subtraction_right_longer(self):
        # Вычитание, когда правый список длиннее
        a = CustomList([10, 20])
        b = CustomList([1, 2, 3, 4])
        result = a - b
        self.assertTrue(is_equal(result, [9, 18, -3, -4]))
        self.assertTrue(is_equal(a, [10, 20]))
        self.assertTrue(is_equal(b, [1, 2, 3, 4]))

    def test_subtraction_with_regular_list(self):
        a = CustomList([10, 20, 30])
        b = [1, 2]
        result = a - b
        self.assertTrue(is_equal(result, [9, 18, 30]))
        self.assertTrue(is_equal(a, [10, 20, 30]))
        self.assertTrue(is_equal(b, [1, 2]))

    def test_rsubtraction_with_regular_list(self):
        a = [10, 20, 30]
        b = CustomList([1, 2])
        result = a - b
        self.assertTrue(is_equal(result, [9, 18, 30]))
        self.assertTrue(is_equal(a, [10, 20, 30]))
        self.assertTrue(is_equal(b, [1, 2]))
