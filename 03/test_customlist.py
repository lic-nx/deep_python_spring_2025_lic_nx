import unittest
import os
import sys
import inspect
from customlist import CustomList


sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestCustomList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nТестированае класса CustomList")

    def test_class_is_create(self):
        self.assertEqual(inspect.isclass(CustomList), True)

    def test_class_is_subclass(self):
        self.assertEqual(issubclass(CustomList, list), True)
    
    def test_from_exsample(self):
        self.assertEqual(CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]), CustomList([6, 3, 10, 7]))
        self.assertEqual(CustomList([10]) + [2, 5], CustomList([12, 5]))
        self.assertEqual([2, 5] + CustomList([10]), CustomList([12, 5]))
        self.assertEqual(CustomList([2, 5]) + 10, CustomList([12, 15]))
        self.assertEqual(10 + CustomList([2, 5]), CustomList([12, 15]))
        self.assertEqual(CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7]), CustomList([4, -1, -4, 7]))
        self.assertEqual(CustomList([10]) - [2, 5], CustomList([8, -5]))
        self.assertEqual([2, 5] - CustomList([10]), CustomList([-8, 5]))
        self.assertEqual(CustomList([2, 5]) - 10 , CustomList([-8, -5]))
        self.assertEqual(10 - CustomList([2, 5]), CustomList([8, 5]))
    
    def test_class_like_list(self):
        cl = CustomList()
        cl.append(4)
        cl.append(5)
        self.assertEqual(cl, [4, 5])
        self.assertIsInstance(cl, CustomList)

    def test_equao(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 4, 3])
        self.assertEqual(cl == other_cl, True)
        cl.append(5)
        self.assertEqual(cl != other_cl, True)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)

    def test_greate_then(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 4, 5])
        self.assertEqual(cl > other_cl, False)
        cl.append(5)
        self.assertEqual(cl > other_cl, True)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)

    def test_less_then(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 4, 5])
        self.assertEqual(cl < other_cl, True)
        cl.append(5)
        self.assertEqual(cl < other_cl, False)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)

    def test_greate_egual_then(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 4, 3])
        self.assertEqual(cl >= other_cl, True)
        cl.append(5)
        self.assertEqual(cl >= other_cl, True)

    def test_less_egual_then(self):
        cl = CustomList([1, 2, 3, 4])
        other_cl = CustomList([1, 2, 3, 4])
        self.assertEqual(cl <= other_cl, True)
        cl.append(5)
        self.assertEqual(cl <= other_cl, False)

    def test_str(self):
        cl = CustomList([1, 2, 3, 4])
        self.assertEqual(str(cl), "CustomList([1, 2, 3, 4]), Sum: 10")

    def test_sub(self):
        cl = CustomList([1, 2, 4])
        res = cl - 2
        self.assertEqual(res, CustomList([-1, 0, 2]))
        self.assertEqual(isinstance(res, CustomList), True)
        other_cl = [1, 1, 1, 1, 1, 1, 1]
        res = cl - other_cl
        self.assertEqual(res, [0, 1, 3, -1, -1, -1, -1])
        self.assertEqual(other_cl, [1, 1, 1, 1, 1, 1, 1])

    def test_rsub(self):
        cl = CustomList([1, 2, 4])
        res = 2 - cl
        self.assertEqual(res, CustomList([1, 0, -2]))
        self.assertEqual(isinstance(res, CustomList), True)
        other_cl = [1, 1, 1, 1, 1, 1, 1]
        res = other_cl - cl
        self.assertEqual(res, [0, -1, -3, 1, 1, 1, 1])

    def test_summ(self):
        cl = CustomList([1, 2, 4])
        res = cl + 2
        self.assertEqual(res, CustomList([3, 4, 6]))
        self.assertEqual(isinstance(res, CustomList), True)
        other_cl = [1, 1, 1, 1, 1, 1, 1]
        res = cl + other_cl
        self.assertEqual(res, [2, 3, 5, 1, 1, 1, 1])
        self.assertIsInstance(res, CustomList)
        self.assertEqual(other_cl, [1, 1, 1, 1, 1, 1, 1])
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)
        
    def test_rsumm(self):
        cl = CustomList([1, 2, 4])
        res = 2 + cl
        self.assertEqual(res, CustomList([3, 4, 6]))
        self.assertEqual(isinstance(res, CustomList), True)
        other_cl = [1, 1, 1, 1, 1, 1, 1]
        res = other_cl + cl
        self.assertEqual(res, [2, 3, 5, 1, 1, 1, 1])
        self.assertEqual(other_cl, [1, 1, 1, 1, 1, 1, 1])
        self.assertIsInstance(res, CustomList)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)

    def test_cl_longest_summ(self):
        cl = CustomList([1, 2, 4, 5])
        self.assertEqual(res, CustomList([3, 4, 6]))
        self.assertEqual(isinstance(res, CustomList), True)
        other_cl = [1, 1]
        res = other_cl + cl
        self.assertEqual(res, [2, 3, 4, 5])
        self.assertEqual(other_cl, [1, 1])
        self.assertIsInstance(res, CustomList)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)

    def test_cl_summ(self):
        cl = CustomList([1, 2, 4, 5])
        self.assertEqual(res, CustomList([3, 4, 6]))
        self.assertEqual(isinstance(res, CustomList), True)
        other_cl = CustomList[1, 1]
        res = other_cl + cl
        self.assertEqual(res, [2, 3, 4, 5])
        self.assertEqual(other_cl, [1, 1])
        self.assertIsInstance(res, CustomList)
        self.assertIsInstance(cl, CustomList)
        self.assertIsInstance(other_cl, CustomList)
