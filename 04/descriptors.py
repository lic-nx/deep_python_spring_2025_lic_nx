# тесты нужно для класса в который помещен дескриптор(
# выбрана тема - компьютерные игры 
# Дескрипторы - Шкала здоровья, элементов в инвентаре, характеристики(например сила, ловкость)

class BaseDescriptor:
    def __set_name__(self, owner, name):
        print(f"set name: {owner=}, {name=}")
        self.name = f"_hidden_int_{owner}_{name}"
        self.default_name = f"_hidden_int_{owner}_{name}_default"

    def __get__(self, obj):
        if obj is None:
            return None
        return obj.__dict__[self.name], obj.__dict__[self.default_name]
        

class HealthBarDescriptor(BaseDescriptor):
    def __init__(self, default=100):
        self.default = default

    def __set__(self, obj, val: int, max_val = None):
        # если персонаж увеличивает макс. значение здоровья
        print(f"set {val} for {obj}")
        if max_val != None and max_val != obj.__dict__[self.default_name]:
            obj.__dict__[self.default_name] = max_val
        val = max(0, min(val, max_val))
        obj.__dict__[self.name] = val


class CharactiristicDescriptor(BaseDescriptor):
    #отражать что за характеристика будет ссылка на дескриптор
    # у разных характеристик персонажа могут быть разные максимальные значения
    def __init__(self, default=0, max_value):
        self.name = default
        self.default_name = charactiristic_name
        
    def __set__(self, obj, val: int):
        if val > obj.__dict__[self.default_name]:
            raise ValueError(f"Значение навыка не может быть больше {obj.__dict__[self.default_name]}")
        if val < 0:
            raise ValueError(f"Значение навыка не может быть отрицательным")
        obj.__dict__[self.name] = val
    
class NameDescriptor(BaseDescriptor):
    def __init__(self, default):
        self.name = default
    
    def __set__(self, obj, val):
        raise ValueErroe("You can't chanje name")

class MainCharacter:
        health = HealthBarDescriptor()
        name = String() #  менять имя в игре нельзя
        power = CharactiristicDescriptor()
        dexterity = CharactiristicDescriptor()
        def __init__(...):
            ....
