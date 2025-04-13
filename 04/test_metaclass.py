import unittest
import inspect
from metaclass import CustomClass, CustomMeta


class TestMetaclass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nТестированае класса Metaclass")

    def test_class_is_create(self):
        self.assertEqual(inspect.isclass(CustomMeta), True)

    def test_class_is_subclass(self):
        self.assertEqual(issubclass(CustomMeta, CustomClass), False)
        self.assertEqual(issubclass(CustomClass, CustomMeta), False)
        self.assertEqual(isinstance(CustomClass, CustomMeta), True)

    def test_underline(self):
        def new_method():
            return "can cal"

        inst = CustomClass()
        # тестирование приватного атрибута
        inst.__exm = "it is examply"
        # тестирование метода
        inst.__new_method = new_method
        # тестирование атрибута, который иммитириует внешний вид магической ф-ии
        inst.__exm_wit_dobl_underline__ = "не магический метод"
        self.assertEqual(inst.custom__TestMetaclass__exm, "it is examply")

        self.assertEqual(inst.custom__TestMetaclass__new_method(), "can cal")
        self.assertEqual(inst.custom___exm_wit_dobl_underline__,
                         "не магический метод")
        with self.assertRaises(AttributeError):
            getattr(inst.__exm_wit_dobl_underline__)
        with self.assertRaises(AttributeError):
            getattr(inst._TestMetaclass__new_method)
        with self.assertRaises(AttributeError):
            getattr(inst.__exm)

    def test_exanple(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            getattr(CustomClass, "x")

        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")

        with self.assertRaises(AttributeError):
            getattr(inst.x)
        with self.assertRaises(AttributeError):
            getattr(inst.val)
        with self.assertRaises(AttributeError):
            getattr(inst.line)
        with self.assertRaises(AttributeError):
            getattr(inst.yyy)
        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError):
            getattr(inst.dynamic)
