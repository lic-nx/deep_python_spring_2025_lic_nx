import re
import sys
from abc import ABC, abstractmethod
# тесты нужно для класса в который помещен дескриптор(
# выбрана тема - компьютерные игры
# Дескрипторы - Шкала здоровья, характеристики(например сила, ловкость), имя


class BaseDescriptor(ABC):  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.value = None

    def __set_name__(self, owner, name):
        self.value = f"_hidden_int_{owner}_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None
        return obj.__dict__[self.value]

    def __set__(self, obj, val):
        new_val = self._validate(val)
        obj.__dict__[self.value] = new_val

    @abstractmethod
    def _validate(self, val):
        pass


class BarDescriptor(BaseDescriptor):  # pylint: disable=too-few-public-methods
    #  измеряем в процентах
    # на персонажа могут накинуть урон
    # который больше его жизней
    # на персонажа могут накинуть дебав,
    # который будет высасывать ману даже при минусе значения

    def _validate(self, val):
        if not isinstance(val, (int, float)):
            raise TypeError(
                "Значение должно быть либо целочисленное,"
                "либо с плавующей точкой"
            )
        # не может быть больше 100% и меньше 0%
        val = max(0, min(val, 100))

        return round(val, 2)


class CharDescriptor(BaseDescriptor):  # pylint: disable=too-few-public-methods
    # отражать что за характеристика будет ссылка на дескриптор
    # считаем, что есть целочисленная шкала навыков умения
    # предолов верхних нет.
    def _validate(self, val):
        # предполагаем, что на шкале навыков игрок может как откатывать умения
        if not isinstance(val, int):
            raise TypeError("принимаются только целочисленные значения")
        if val > sys.maxsize:
            raise ValueError("слишком большое значение")
        if val < 0:
            raise ValueError("Значение навыка не может быть отрицательным")
        return val


class NameDescriptor(BaseDescriptor):  # pylint: disable=too-few-public-methods
    def _validate(self, value):
        # в имени не должно быть цифр или спц. символов кроме точки и тире
        # mr.Martin тоже считаем за имя
        if not isinstance(value, str):
            raise TypeError("принимаются только строки")
        name = value.lower()
        pattern = r"^[a-zа-я '.-]*[a-zа-я][a-zа-я '.-]*$"
        if not re.match(pattern, name):
            raise ValueError("Имя не подходит")
        return name.title()


class Character:  # pylint: disable=too-few-public-methods
    health = BarDescriptor()
    magic = BarDescriptor()
    name = NameDescriptor()
    power = CharDescriptor()
    dexterity = CharDescriptor()

    def __init__(self,  # pylint: disable=too-many-arguments
                 name="John Doe",
                 health=100,
                 magic=100,
                 power=0,
                 dexterity=0):
        self.name = name
        self.health = health
        self.magic = magic
        self.power = power
        self.dexterity = dexterity
