# Priority Queue implementation in heap tree (min-heap)

import math
from typing import List, TypeVar, Callable

T = TypeVar('T')


class PriorityHeapQueue:
    def __init__(self, elements: List[T], comparator: Callable[[T, T], float]):
        self.queue: List[T] = elements
        self.comparator: Callable[[T, T], float] = comparator

    def heapify_tree(self):
        for index in reversed(range(math.ceil(len(self.queue) / 2) - 1)):
            self.heapify(index)

    def insert(self, element: T):
        self.queue.append(element)
        self.insertion_heapify(len(self.queue) - 1)

    def pop(self):
        self.heapify_tree()
        self.swap(0, len(self.queue) - 1)
        element = self.queue.pop()
        self.heapify(0)
        return element

    # heapify after insertion
    # check if the parent node is smaller than the inserted node
    # if yes, keep heapify the parent node until the parent node is larger than the child node
    def insertion_heapify(self, index: int):
        parent_node = math.floor((index - 1) / 2)
        if parent_node < 0:
            return
        if self.comparator(self.queue[index], self.queue[parent_node]) < 0:
            self.swap(parent_node, index)
            self.insertion_heapify(parent_node)

    def heapify(self, index: int):
        smallest = index
        left_node = index * 2 + 1
        right_node = index * 2 + 2
        if left_node < len(self.queue) and self.comparator(self.queue[left_node], self.queue[smallest]) < 0:
            smallest = left_node
        if right_node < len(self.queue) and self.comparator(self.queue[right_node], self.queue[smallest]) < 0:
            smallest = right_node
        if index != smallest:
            self.swap(index, smallest)
            self.heapify(smallest)

    def swap(self, first: int, second: int):
        temp: T = self.queue[first]
        self.queue[first] = self.queue[second]
        self.queue[second] = temp

    def is_empty(self):
        return len(self.queue) == 0

    def queue_debug(self):
        print(', '.join(map(lambda element: str(element), self.queue)))


def comparator(i: int, j: int) -> float:
    return i - j


if __name__ == '__main__':
    priority_queue = PriorityHeapQueue([20, 14, 3, 1, 11, 7], comparator)
    print('initial insertion')
    priority_queue.queue_debug()
    priority_queue.insert(6)
    priority_queue.insert(5)
    print('after inserting 6 and 5')
    priority_queue.queue_debug()
    priority_queue.pop()
    priority_queue.queue_debug()
