import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):

    def test_cache_initially_empty(self):
        cache = LRUCache(2)
        self.assertIsNone(cache.get("k1"))

    def test_set_and_get_single_value(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        self.assertEqual(cache.get("k1"), "val1")

    def test_cache_evicts_lru_when_full(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")

    def test_access_updates_most_recently_used(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.get("k1")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k3"), "val3")

    def test_overwrite_existing_key(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k1", "new_val1")
        self.assertEqual(cache.get("k1"), "new_val1")

    def test_order_after_get(self):
        cache = LRUCache(4)
        cache.set("a", "A")
        cache.set("b", "B")
        cache.set("c", "C")
        cache.get("a")
        cache.set("d", "D")

        self.assertEqual(cache.get("d"), "D")
        self.assertEqual(cache.get("a"), "A")
        self.assertEqual(cache.get("b"), "B")
        self.assertEqual(cache.get("c"), "C")

    def test_initial_state(self):
        """Проверяем начальное состояние"""
        cache = LRUCache(3)
        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache._LRUCache__size, 0)
        self.assertEqual(len(cache._LRUCache__lru_cash), 0)

    def test_add_single_element(self):
        """Добавляем один элемент"""
        cache = LRUCache(3)
        cache.set("k1", "val1")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache._LRUCache__head.key, "k1")
        self.assertEqual(cache._LRUCache__end.key, "k1")

    def test_update_existing_key_value(self):
        """Обновление существующего ключа"""
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k1", "new_val1")
        self.assertEqual(cache.get("k1"), "new_val1")
        self.assertEqual(cache._LRUCache__head.key, "k1")
        self.assertEqual(cache._LRUCache__end.key, "k1")

    def test_access_moves_to_front(self):
        """При вызове get() элемент перемещается в начало"""
        cache = LRUCache(3)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        cache.get("k2")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache._LRUCache__head.key, "k2")
        self.assertEqual(cache._LRUCache__head.next.key, "k3")
        self.assertEqual(cache._LRUCache__end.key, "k1")

    def test_eviction_order_after_multiple_accesses(self):
        """Проверяем порядок вытеснения после нескольких обращений"""
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.get("k1")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k3"), "val3")

    def test_full_replacement(self):
        """Проверяем полную замену кэша"""
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        cache.set("k4", "val4")

        self.assertEqual(cache.get("k4"), "val4")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertIsNone(cache.get("k1"))

    def test_edge_case_one_capacity(self):
        """Тест для кэша с вместимостью 1"""
        cache = LRUCache(1)
        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache.get("k2"), "val2")

    def test_lru_with_multiple_sets(self):
        """Многократные set одного и того же ключа"""
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k1", "updated_val1")
        cache.set("k3", "val3")

        self.assertEqual(cache.get("k1"), "updated_val1")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k3"), "val3")
