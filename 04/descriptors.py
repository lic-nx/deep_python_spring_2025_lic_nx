# тесты нужно для класса в который помещен дескриптор(
# выбрана тема - компьютерные игры 
# Дескрипторы - Шкала здоровья, элементов в инвентаре, позиция в мире

class HealthBarDescriptor:
    def __init__(self, default=100):
        self.default = default

    def __set_name__(self, owner, name):
        print(f"set name: {owner=}, {name=}")
        self.name = f"_hidden_int_{owner}_{name}"
        self.default_name = f"_hidden_int_{owner}_{name}_default"


    def __get__(self, obj):
        if obj is None:
            return None
        return obj.__dict__[self.name], obj.__dict__[self.default_name]
        # return getattr(obj, self.name)

    def __set__(self, obj, val, max_val = None):
        # если персонаж увеличивает макс. значение здоровья
        print(f"set {val} for {obj}")
        if max_val != None and max_val != obj.__dict__[self.default_name]:
            obj.__dict__[self.default_name] = max_val
        if not isinstance(val, int):
            raise ValueError("wrong value of health")
        val = max(0, min(val, max_val))
        obj.__dict__[self.name] = val



class MainCharacter:
        health = HealthBarDescriptor()
        name = String()
        price = PositiveInteger()

        def __init__(...):
            ....