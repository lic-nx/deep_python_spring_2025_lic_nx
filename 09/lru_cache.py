"""упражнение на логирование"""

import logging
import argparse


logger = logging.getLogger(__name__)
logging.basicConfig(filename="cache.log", level=logging.DEBUG)


# pylint: disable=R0903
class Node:
    """Node"""

    def __init__(self, key, val, following=None, before=None):
        self.key = key
        self.val = val
        self.following = following
        self.before = before


class LRUCache:
    """LRUCache"""

    def __init__(self, limit=42):
        logger.info("Создался класс")
        if not isinstance(limit, int):
            logger.error("Ограничение должно быть целочисленным")
            raise TypeError("Limit must be an integer")
        if limit <= 0:
            logger.error("Ограничение должно быть больше 0")
            raise ValueError("Limit must be greater than zero")
        self.__limit = limit
        self.__size = 0
        self.__lru_cash = {}
        self.__head = None
        self.__end = None

    def show(self):
        """Вывод текущего состояния"""
        logger.info("Отображение текущего состояния кэша")
        print("\nLRU Cache State:")
        print("+------+-------+--------------+--------------+")
        print("| KEY  | VAL   | following | PREV |")
        print("+------+-------+--------------+--------------+")

        current = self.__head
        while current:
            key = str(current.key).ljust(4)
            val = str(current.val).ljust(5)
            following_key = str(
                current.following.key if current.following else None
            ).ljust(12)
            prev_key = str(current.before.key
                           if current.before
                           else None).ljust(12)

            print(f"| {key} | {val} | {following_key} | {prev_key} |")
            current = current.following

        print("+------+-------+--------------+--------------+\n")

    def get(self, key):
        """получение значения по ключу"""
        logger.info("Получение значения по ключу")
        logger.debug("Нужно вернуть значение для %i", key)
        if key in self.__lru_cash:
            self.__replase_to_front(key)
            logger.debug("Возвращаем значение %i", self.__head.val)
            return self.__head.val
        return None

    def set(self, key, value):
        """Добавление новых ключей значений"""
        logger.debug("Пришли значения %i, %i", key, value)
        if key in self.__lru_cash:
            self.__replase_to_front(key)
            self.__lru_cash[key].val = value
        else:
            if self.__size == self.__limit:
                self.__remuve_end()
            self.__add_to_front(value, key)

    def __add_to_front(self, value, key):
        logger.info("Добавление элемента в начало %i", key)
        node = Node(key, value, self.__head)
        if len(self.__lru_cash) == 0:
            self.__head = self.__end = node
        else:
            self.__head.before = node
            self.__head = node
        self.__lru_cash[key] = node
        self.__size += 1

    def __remuve_end(self):
        logger.info("Удаление последнего элемента")
        if len(self.__lru_cash) == 1:
            self.__lru_cash.pop(self.__end.key)
            self.__end = None
            self.__head = None
        else:
            self.__lru_cash.pop(self.__end.key)
            self.__end = self.__end.before
            del self.__end.following
            self.__end.following = None
            self.__size -= 1

    def __replase_to_front(self, key):
        logger.info("Перемещение элемента в начало %i", key)
        node = self.__lru_cash[key]
        if node.before is None:
            logger.info("Первое значение")
            return
        if node.following is None:
            self.__end.following = self.__head
            self.__end.before.following = None
            self.__head.before = self.__end
            self.__end = self.__end.before
            self.__head = self.__head.before
        else:
            node.before.following = node.following
            node.following.before = node.before
            node.before = None
            node.following = self.__head
            self.__head.before = node
            self.__head = node


class CustomFilter(logging.Filter):
    """Класс фильтра"""

    def filter(self, record):
        #  пропускаем только сообщения с нечетным числом слов
        message = record.getMessage()
        word_count = len(message.split())
        return word_count % 2 != 0


def settings(logs_args):
    """настройки для логирования"""
    if logs_args.stdout:
        # По аргументу командной строки "-s" дополнительно
        # логировать в stdout с отдельным форматированием.
        cons_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        cons_handler.setFormatter(formatter)
        logger.addHandler(cons_handler)
    #  "-f" нужно применять кастомный фильтр, например
    if logs_args.filter:
        logger.addFilter(CustomFilter())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--stdout",
        action="store_true",
        help="логгирование в sdtout"
    )
    parser.add_argument("-f",
                        "--filter",
                        action="store_true",
                        help="кастомный фильтр")
    args = parser.parse_args()
    settings(args)
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k2", "val2.1")
    assert cache.get("k2") == "val2.1"
    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k1") is None
    assert cache.get("k2") == "val2.1"
