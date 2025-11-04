import sys
import unittest
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10 ** 6)
from bst import *


@dataclass(frozen=True)
class Point2:
    x: float
    y: float

    def radius2(self) -> float:
        return self.x ** 2 + self.y ** 2


class BSTTests(unittest.TestCase):
    def build_tree(self, cb: Callable[[Any, Any], bool], values: Iterable[Any]) -> BinarySearchTree:
        t = BinarySearchTree(None, cb)
        for v in values:
            t = insert(t, v)
        return t

    def test_is_empty_on_new_and_after_insert(self):
        cb = lambda a, b: a < b
        t = BinarySearchTree(None, cb)
        self.assertTrue(is_empty(t))
        t = insert(t, 1)
        self.assertFalse(is_empty(t))

    def test_numeric_insertion_structure_and_lookup(self):
        cb = lambda a, b: a < b
        values = [5, 3, 7, 2, 4, 6, 8, 3]
        t = self.build_tree(cb, values)

        for v in [5, 3, 2, 4, 6, 7, 8]:
            self.assertTrue(lookup(t, v))
        self.assertFalse(lookup(t, 9))

        expected = Node(
            5,
            Node(
                3,
                Node(2, None, None),
                Node(
                    4,
                    None,
                    None
                )
            ),
            Node(
                7,
                Node(6, None, None),
                Node(8, None, None)
            )
        )

        expected_with_dup = Node(
            5,
            Node(
                3,
                Node(2, None, None),
                Node(
                    4,
                    Node(3, None, None),
                    None
                )
            ),
            Node(
                7,
                Node(6, None, None),
                Node(8, None, None)
            )
        )

        self.assertEqual(t.tree, expected_with_dup)

    def test_numeric_delete_cases(self):
        cb = lambda a, b: a < b
        t = self.build_tree(cb, [5, 3, 7, 2, 4, 6, 8, 3])

        t1 = delete(t, 3)
        self.assertTrue(lookup(t1, 3))

        t2 = delete(t1, 3)
        self.assertFalse(lookup(t2, 3))

        self.assertTrue(lookup(t2, 2))
        t3 = delete(t2, 2)
        self.assertFalse(lookup(t3, 2))

        self.assertTrue(lookup(t3, 7))
        t4 = delete(t3, 7)
        self.assertFalse(lookup(t4, 7))
        self.assertTrue(lookup(t4, 8))

        self.assertTrue(lookup(t4, 5))
        t5 = delete(t4, 5)
        self.assertFalse(lookup(t5, 5))

    def test_string_ordering(self):
        cb = lambda a, b: a < b
        t = self.build_tree(cb, ["d", "b", "f", "a", "c", "e", "g"])

        for s in ["a", "b", "c", "d", "e", "f", "g"]:
            self.assertTrue(lookup(t, s))
        for s in ["", "z", "aa"]:
            self.assertFalse(lookup(t, s))

        t1 = delete(t, "d")
        self.assertFalse(lookup(t1, "d"))
        self.assertTrue(all(lookup(t1, s) for s in ["a", "b", "c", "e", "f", "g"]))

    def test_point_distance_ordering_lookup_and_delete(self):
        def cb(a: Point2, b: Point2) -> bool:
            return a.radius2() < b.radius2()

        p1 = Point2(1, 0)
        p2 = Point2(0, 2)
        p3 = Point2(-3, 0)
        t = self.build_tree(cb, [p2, p1, p3])

        p2_alt = Point2(2, 0)
        self.assertTrue(lookup(t, p2_alt))

        t1 = delete(t, p2_alt)
        self.assertFalse(lookup(t1, p2))
        self.assertTrue(lookup(t1, p1))
        self.assertTrue(lookup(t1, p3))


if __name__ == '__main__':
    unittest.main()
