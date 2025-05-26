### 1. Сравнение использования weakref и слотов
# Нужно придумать свои типы с несколькими атрибутами:
# - класс с обычными атрибутами
# - класс со слотами
# - класс с атрибутами weakref

# Для каждого класса создается большое число экземпляров и замеряется (сравнивается):
# - время создания пачки экземпляров;
# - время чтения/изменения атрибутов пачки экземпляров.

# Результаты замеров оформляются скриншотами c описанием и выводом.
import gc
import time
gc.disable()

class UsualClass:
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2

class SlotsClass:
    __slots__ = ['attr1', 'attr2']
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2

class WeakrefClass:
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2

    # def __del__(self):
    #     print(f"Instance of WeakrefClass with attr1={self.attr1} is being deleted")

example_create_time = {}
num_instances = 10000

start_time = time.time()
usual_class = [UsualClass(i, i**2) for i in range(num_instances)]
end_time = time.time()
example_create_time["usual_class_time"] = end_time - start_time

start_time = time.time()
slots_class = [SlotsClass(i, i**2) for i in range(num_instances)]
end_time = time.time()
example_create_time["slots_class_time"] = end_time - start_time

start_time = time.time()
weakref_class = [WeakrefClass(i, i**2) for i in range(num_instances)]
end_time = time.time()
example_create_time["weakref_class_time"] = end_time - start_time

print(example_create_time["usual_class_time"], example_create_time["slots_class_time"], example_create_time["weakref_class_time"])
gc.enable()