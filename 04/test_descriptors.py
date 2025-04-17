import unittest
import inspect
import sys
from descriptors import Character


class TestMetaclass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nТестированае класса дескрипторов")

    def test_class_is_create(self):
        self.assertEqual(inspect.isclass(Character), True)

    def test_class_test_health(self):
        player = Character(health=110, magic=99)
        player.health = 110
        self.assertEqual(player.health, 100)
        self.assertEqual(player.magic, 99)
        player.health = -1
        self.assertEqual(player.health, 0)
        self.assertEqual(player.magic, 99)
        with self.assertRaises(TypeError):
            Character('Steeve', "0.2")
        player.health -= 1000
        self.assertEqual(player.health, 0)
        self.assertEqual(player.magic, 99)
        player.health += 10
        self.assertEqual(player.health, 10)
        self.assertEqual(player.magic, 99)
        player.health += 1000
        self.assertEqual(player.health, 100)
        self.assertEqual(player.magic, 99)
        player.health -= 999
        player.health += 1000
        self.assertEqual(player.health, 100)
        self.assertEqual(player.magic, 99)
        player.health /= 2
        self.assertEqual(player.health, 50)
        player.health *= 0.5
        self.assertEqual(player.health, 25)
        player.health *= 1000
        self.assertEqual(player.health, 100)
        player.health -= 0.5
        self.assertEqual(player.health, 99.5)
        player.health = 0
        self.assertEqual(player.health, 0)
        self.assertEqual(player.magic, 99)
        player.health = -1000
        player.magic += 15
        self.assertEqual(player.health, 0)
        self.assertEqual(player.magic, 100)
        player.magic /= 5
        self.assertEqual(player.magic, 20)
        self.assertEqual(player.health, 0)
        self.assertEqual(player.magic, 20)
        self.assertEqual(player.health, 0)

    def test_errors_bar(self):
        player = Character(health=110, magic=99)
        with self.assertRaises(TypeError):
            player.magic = 'dffd'
        with self.assertRaises(TypeError):
            player.health = 'dffd'
        self.assertEqual(player.magic, 99)
        self.assertEqual(player.health, 100)

    def test_so_small(self):
        player = Character(health=110, magic=99)
        player.health = 0.000000001
        player.magic += 15
        self.assertEqual(player.health, 0.00)
        self.assertEqual(player.magic, 100)

    def test_class_test_name(self):
        player = Character()
        self.assertEqual(player.name, "John Doe")
        player.name = "bob"
        self.assertEqual(player.name, "Bob")
        player.name = "mr. Watson"
        self.assertEqual(player.name, "Mr. Watson")
        player.name = "Karabas-barabas"
        self.assertEqual(player.name, "Karabas-Barabas")
        player.name = "ГоРн"
        self.assertEqual(player.name, "Горн")
        player.name = "Ю'Берион"
        self.assertEqual(player.name, "Ю'Берион")
        player.name = "ИдОЛ каДАР"
        self.assertEqual(player.name, "Идол Кадар")
        with self.assertRaises(ValueError):
            player.name = "123456"
        with self.assertRaises(ValueError):
            player.name = "Ди3е4го"
        with self.assertRaises(ValueError):
            player.name = ""
        with self.assertRaises(TypeError):
            player.name = 23
        with self.assertRaises(TypeError):
            player.name = True
        with self.assertRaises(TypeError):
            player.name = 20.44
        player.name = "Чио-Чио-сан"
        self.assertEqual(player.name, "Чио-Чио-Сан")
        Character()
        self.assertEqual(Character.name, None)

    def test_class_test_power_dexterity(self):
        player = Character()
        with self.assertRaises(TypeError):
            player.power = 'dffd'
        with self.assertRaises(TypeError):
            player.dexterity = 'dffd'
        with self.assertRaises(TypeError):
            player.power = 1.2
        with self.assertRaises(TypeError):
            player.dexterity = 1.5
        player.dexterity = 7
        self.assertEqual(player.dexterity, 7)
        self.assertEqual(player.power, 0)
        player.power += 15
        self.assertEqual(player.dexterity, 7)
        self.assertEqual(player.power, 15)
        with self.assertRaises(ValueError):
            player.dexterity = -45
        with self.assertRaises(ValueError):
            player.dexterity = -45
        self.assertEqual(player.dexterity, 7)
        self.assertEqual(player.power, 15)
        player.dexterity *= 7
        player.power += 1500
        self.assertEqual(player.dexterity, 49)
        self.assertEqual(player.power, 1515)
        with self.assertRaises(ValueError):
            player.dexterity = 92233720368547758075
        player.power = 1
        self.assertEqual(player.power, 1)


    def test_characteristic_descriptor(self):
        character1 = Character(name="Hero-first", health=80, magic=90, power=10, dexterity=5)
        character2 = Character(name="Hero-second", health=70, magic=80, power=20, dexterity=15)
        character1.power = 30
        self.assertEqual(character1.power, 30)
        self.assertEqual(character2.power, 20)
        with self.assertRaises(ValueError) as cm:
            character1.power = -5
        self.assertEqual(str(cm.exception), "Значение навыка не может быть отрицательным")
        self.assertEqual(character1.power, 30)
        with self.assertRaises(ValueError) as cm:
            character1.power = sys.maxsize + 1
        self.assertEqual(str(cm.exception), "слишком большое значение")
        self.assertEqual(character1.power, 30)
        with self.assertRaises(TypeError) as cm:
            character1.power = "invalid"
        self.assertEqual(str(cm.exception), "принимаются только целочисленные значения")
        self.assertEqual(character1.power, 30)
