class Node:
    def __init__(self, key, val, next=None, before=None):
        self.key = key
        self.val = val
        self.next = next
        self.before = before


class LRUCache:
    def __init__(self, limit=42):
        if not isinstance(limit, int):
            raise TypeError("Limit must be an integer")
        if limit <= 0:
            raise ValueError("Limit must be greater than zero")
        self.__limit = limit
        self.__size = 0
        self.__lru_cash = {}
        self.__head = None
        self.__end = None

    def show(self):
        print("\nLRU Cache State:")
        print("+------+-------+--------------+--------------+")
        print("| KEY  | VAL   | NEXT         | PREV         |")
        print("+------+-------+--------------+--------------+")

        current = self.__head
        while current:
            key = str(current.key).ljust(4)
            val = str(current.val).ljust(5)
            next_key = str(current.next.key if current.next else None).ljust(12)
            prev_key = str(current.before.key if current.before else None).ljust(12)

            print(f"| {key} | {val} | {next_key} | {prev_key} |")
            current = current.next

        print("+------+-------+--------------+--------------+\n")

    def get(self, key):
        if key in self.__lru_cash.keys():
            # print("print key", key, self.__lru_cash.keys())
            self.__replase_to_front(key)
            return self.__head.val
        return None

    def set(self, key, value):
        if key in self.__lru_cash.keys():
            self.__replase_to_front(key)
            self.__lru_cash[key].val = value
        else:
            if self.__size == self.__limit:
                self.__remuve_end()
            self.__add_to_front(value, key)

    def __add_to_front(self, value, key):
        node = Node(key, value, self.__head)
        if len(self.__lru_cash) == 0:
            self.__head = self.__end = node
        else:
            self.__head.before = node
            self.__head = node
        self.__lru_cash[key] = node
        self.__size += 1

    def __remuve_end(self):
        if len(self.__lru_cash) == 1:
            self.__lru_cash.pop(self.__end.key)
            self.__end = None
            self.__head = None
        else:
            self.__lru_cash.pop(self.__end.key)
            self.__end = self.__end.before
            del self.__end.next
            self.__end.next = None
            self.__size -= 1

    def __replase_to_front(self, key):
        node = self.__lru_cash[key]
        if node.before is None:
            return
        elif node.next is None:
            self.__end.next = self.__head
            self.__end.before.next = None
            self.__head.before = self.__end
            self.__end = self.__end.before
            self.__head = self.__head.before
        else:
            node.before.next = node.next
            node.next.before = node.before
            node.before = None
            node.next = self.__head
            self.__head.before = node
            self.__head = node


if __name__ == "__main__":
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"
