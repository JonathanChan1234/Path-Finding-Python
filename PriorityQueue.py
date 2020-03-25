import sys
from typing import List, Tuple
from Node import Node


# Priority Queue Implementation using the list data structure
class PriorityQueue(object):
    def __init__(self):
        self.queue: List[Node] = []

    def __str__(self):
        return ',\n'.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def insert(self, item: Node):
        self.queue.append(item)

    def pop(self) -> Tuple[int, int]:
        try:
            min_index = 0
            min = sys.maxsize
            for i in range(len(self.queue)):
                if self.queue[i].get_distance() < min:
                    min_index = i
                    min = self.queue[i].get_distance()
            x = self.queue[min_index].x
            y = self.queue[min_index].y
            del self.queue[min_index]
            return x, y
        except IndexError:
            print("Index Error")
            exit()
