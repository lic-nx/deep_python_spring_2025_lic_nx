"""задание 1 и 2"""

import gc
import time
import weakref
from tabulate import tabulate
from memory_profiler import profile

gc.collect()
gc.disable()


# pylint: disable=R0903
class EmptyClass:
    """Класс заглушка"""

    def __init__(self):
        self.attr1 = 1
        self.attr2 = 2


# pylint: disable=R0903
class UsualClass:
    """Обычный класс"""

    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


# pylint: disable=R0903
class SlotsClass:
    """Класс со слотами"""

    __slots__ = ["attr1", "attr2"]

    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


# pylint: disable=R0903
class WeakrefClass:
    """Класс со слабыми ссылками"""

    def __init__(self, attr1, attr2):
        self.attr1 = weakref.ref(attr1)
        self.attr2 = weakref.ref(attr2)


NUM_INSTANCES = 1000000
example_create_time = {}


@profile
def create_usual_class():
    """Создание списка экземпляров UsualClass"""
    usual_class = [UsualClass(i, i**2) for i in range(NUM_INSTANCES)]
    return usual_class


@profile
def create_slots_class():
    """Создание списка экземпляров SlotsClass"""
    slots_class = [SlotsClass(i, i**2) for i in range(NUM_INSTANCES)]
    return slots_class


@profile
def create_weakref_class(usual_class):
    """Создание списка экземпляров WeakrefClass"""
    weakref_class = [WeakrefClass(i, i) for i in usual_class]
    return weakref_class


@profile
def use_usual_class(usual_class):
    """Изменение атрибутов экземпляров UsualClass"""
    for value in usual_class:
        value.attr1 = 7
        value.attr2 = value.attr1 + value.attr2


@profile
def use_slots_class(slots_class):
    """Изменение атрибутов экземпляров SlotsClass"""
    for value in slots_class:
        value.attr1 = 7
        value.attr2 = value.attr1 + value.attr2


@profile
def use_weak_class(weakref_class, emp_class):
    """Изменение атрибутов экземпляров WeakrefClass"""
    for value in weakref_class:
        value.attr1 = weakref.ref(emp_class)
        value.attr2 = weakref.ref(emp_class)


def run():
    """Запуск всех тестов"""
    emp_class = EmptyClass()
    start_time = time.time()
    usual_class = create_usual_class()
    end_time = time.time()
    example_create_time["usual_class_time"] = end_time - start_time

    start_time = time.time()
    slots_class = create_slots_class()
    end_time = time.time()
    example_create_time["slots_class_time"] = end_time - start_time

    start_time = time.time()
    weakref_class = create_weakref_class(usual_class)
    end_time = time.time()
    example_create_time["weakref_class_time"] = end_time - start_time

    start_time = time.time()
    use_usual_class(usual_class)
    end_time = time.time()
    example_create_time["usual_class_read_time"] = end_time - start_time

    start_time = time.time()
    use_slots_class(slots_class)
    end_time = time.time()
    example_create_time["slots_class_read_time"] = end_time - start_time

    start_time = time.time()
    use_weak_class(weakref_class, emp_class)
    end_time = time.time()
    example_create_time["weakref_class_read_time"] = end_time - start_time


if __name__ == "__main__":
    run()
    table_data = [
        ["Класс", "Время создания (сек.)", "Время изменения атрибутов"],
        [
            "UsualClass",
            f"{example_create_time['usual_class_time']:.6f}",
            f"{example_create_time['usual_class_read_time']:.6f}",
        ],
        [
            "SlotsClass",
            f"{example_create_time['slots_class_time']:.6f}",
            f"{example_create_time['slots_class_read_time']:.6f}",
        ],
        [
            "WeakrefClass",
            f"{example_create_time['weakref_class_time']:.6f}",
            f"{example_create_time['weakref_class_read_time']:.6f}",
        ],
    ]
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    gc.enable()
