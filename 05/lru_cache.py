class Node:
    def __init__(self, key, val, next=None, before=None):
        self.key = key
        self.val = val
        self.next = next
        self.before = before

class LRUCache:
        def __init__(self, limit=42):
            self.limit = limit
            self.size = 0
            self.cash = {}
            self.head = None
            self.end = None

        def get(self, key):
            if key in self.cash.keys():
                print("print key", key , self.cash.keys())
                self.__replase_to_front(key)
                return self.head.val
            return None

        def set(self, key, value):
            if key in self.cash.keys() and self.cash[key].value == value:
                self.__replase_to_front(key)
            else:
                if self.size == self.limit:
                    self.__remuve_end()
                self.__add_to_front(value, key)
        
        def __add_to_front(self, value, key):
            node = Node(key, value, self.head)
            if len(self.cash) == 0:
                self.head = self.end = node
            else:
                self.head.before = node
                self.head = node
            self.cash[key] = node
            self.size += 1
        
        def __remuve_end(self):
            # self.end.before.next = None
            self.cash.pop(self.end.key)
            self.end  = self.end.before
            del self.end.next
            self.end.next = None
            self.size -= 1

        def __replase_to_front(self, key):
            node = self.cash[key]
            if node.next is None:
                self.end.next = self.head
                self.end.before.next = None
                self.head.before = self.end
                self.end = self.end.before
                self.head = self.head.before
            elif node.before is None:
                return
            else: 
                node.before.next = node.next
                node.next.before = node.before
                node.before = None
                node.next = self.head
                self.head.before = node
                self.head = node

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