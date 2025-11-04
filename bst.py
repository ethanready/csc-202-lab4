import sys
import unittest
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10 ** 6)

BinTree: TypeAlias = Optional['Node']

@dataclass(frozen=True)
class Node:
    value: Any
    left: BinTree
    right: BinTree


@dataclass(frozen=True)
class BinarySearchTree:
    tree: BinTree
    comes_before: Callable[[Any, Any], bool]


def is_empty(bst: BinarySearchTree) -> bool:
    return bst.tree is None


def insert(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    def helper(tree: BinTree, value: Any) -> BinTree:
        if tree is None:
            return Node(value, None, None)
        if bst.comes_before(value, tree.value):
            return Node(tree.value, helper(tree.left, value), tree.right)
        else:
            return Node(tree.value, tree.left, helper(tree.right, value))

    return BinarySearchTree(helper(bst.tree, value), bst.comes_before)


def lookup(bst: BinarySearchTree, value: Any) -> bool:
    def helper(tree: BinTree, value: Any) -> bool:
        if tree is None:
            return False

        if bst.comes_before(value, tree.value):
            return helper(tree.left, value)
        if bst.comes_before(tree.value, value):
            return helper(tree.right, value)

        return True

    return helper(bst.tree, value)


def delete(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    # Returns (min value, tree w/o min value)
    def extract_min(node: Node) -> Tuple[Any, BinTree]:
        if node.left is None:
            return node.value, node.right
        min_val, new_left = extract_min(node.left)
        return min_val, Node(node.value, new_left, node.right)

    def helper(tree: BinTree, value: Any) -> BinTree:
        if tree is None:
            return None
        if bst.comes_before(value, tree.value):
            return Node(tree.value, helper(tree.left, value), tree.right)
        if bst.comes_before(tree.value, value):
            return Node(tree.value, tree.left, helper(tree.right, value))
        if tree.left is None:
            return tree.right
        if tree.right is None:
            return tree.left
        min_val, new_right = extract_min(tree.right)
        return Node(min_val, tree.left, new_right)

    return BinarySearchTree(helper(bst.tree, value), bst.comes_before)
