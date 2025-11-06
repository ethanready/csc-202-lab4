import sys
import unittest
from typing import *
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import time


sys.setrecursionlimit(10 ** 6)
from bst import *

TREES_PER_RUN: int = 10000


def example_graph_creation() -> None:
    # Return log-base-2 of 'x' + 5.
    def f_to_graph(x: float) -> float:
        return math.log2(x) + 5.0

    # here we're using "list comprehensions": more of Python's
    # syntax sugar.
    x_coords: List[float] = [float(i) for i in range(1, 100)]
    y_coords: List[float] = [f_to_graph(x) for x in x_coords]
    # Could have just used this type from the start, but I want
    # to emphasize that 'matplotlib' uses 'numpy''s specific array
    # type, which is different from the built-in Python array
    # type.
    x_numpy: np.ndarray = np.array(x_coords)
    y_numpy: np.ndarray = np.array(y_coords)
    plt.plot(x_numpy, y_numpy, label='log_2(x)')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Example Graph")
    plt.grid(True)
    plt.legend()  # makes the 'label's show up
    plt.show()

# generates a bst with the given number of random values
def random_tree(n : int) -> BinarySearchTree:
    bst = BinarySearchTree(None, comes_before=lambda a, b : a < b)
    def helper(bst : BinarySearchTree, remaining : int) -> BinarySearchTree:
        if remaining == 0:
            return bst
        new_val = random.random()
        bst = insert(bst, new_val)
        return helper(bst, remaining - 1)
    return helper(bst, n)

# gets the height of a bst
def height(bst : BinarySearchTree) -> int:
    def helper(tree: BinTree) -> int:
        if tree is None:
            return 0
        return 1+ max(helper(tree.left), helper(tree.right))
    return helper(bst.tree)

# finds the max value of n where the total time taken to generate
# a random tree with value n it takes 1.5 to 2.5 seconds
def find_n_max() -> int:
    n = 10
    while True:
        start = time.time()
        for _ in range(TREES_PER_RUN):
            t = random_tree(n)
            height(t)
            
        elapsed = time.time() - start
        if 1.5 <= elapsed <= 2.5:
            print(f"n_max = {n}")
            return n
        elif elapsed > 2.5:
            print(f"To slow at n = {n}")
            return n - 5
        n += 5

# Creates the graph that compares the size of
# n to the average height of random_tree(n)
def graph_avg_heights():
    n_max = find_n_max()
    Ns = np.linspace(0, n_max, 50, dtype=int)
    avg_heights : List[float] = []

    for N in Ns:
        total_height = 0
        for _ in range(TREES_PER_RUN):
            t = random_tree(N)
            total_height += height(t)
        avg_height = total_height / TREES_PER_RUN
        avg_heights.append(avg_height)

    plt.clf()
    plt.xlabel("N (# of Nodes)")
    plt.ylabel("Average Tree Height")
    plt.plot(Ns, avg_heights)
    plt.title("Average Height of Random BSTs vs N")
    plt.grid(True)
    plt.savefig('graph_avg_heights.png')
    print("finished graph")


# finds the max value of n where the total time taken to generate a random tree
# with value n and insert a random value into that tree it takes 1.5 to 2.5 seconds
def find_n_max_insert() -> int:
    n = 10
    while True:
        start = time.time()
        for _ in range(TREES_PER_RUN):
            t = random_tree(n)
            new_val = random.random()
            start_insert = time.time()
            insert(t, new_val)
            _ = time.time() - start_insert
        elapsed = time.time() - start
        if 1.5 <= elapsed <= 2.5:
            print(f"n_max = {n}")
            return n
        elif elapsed > 2.5:
            print(f"Too slow at n = {n}")
            return n - 5
        n += 5

# Creates a graph that compares the size of n to the 
# average time of insert(random_val, random_tree(n))
def graph_avg_insert_time():
    n_max = find_n_max_insert()
    Ns = np.linspace(0, n_max, 50, dtype=int)
    avg_times : List[float] = []

    for N in Ns:
        total_time = 0
        for _ in range(TREES_PER_RUN):
            t = random_tree(N)
            val = random.random()
            start_time = time.time()
            insert(t, val)
            total_time += (time.time() - start_time)
        avg_time = total_time / TREES_PER_RUN
        avg_times.append(avg_time)

    # Plot only after data collection so x and y lengths match
    plt.clf()
    plt.xlabel("N (# of Nodes)")
    plt.ylabel("Average Insert Time (sec)")
    plt.plot(Ns, avg_times)
    plt.title("Average Time to Insert into Random BST vs N")
    plt.grid(True)
    plt.savefig('graph_avg_insert_time.png')
    print("finished graph")
    


if (__name__ == '__main__'):
    graph_avg_heights()
    graph_avg_insert_time()
