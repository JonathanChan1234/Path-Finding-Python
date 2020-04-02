from __future__ import annotations

import sys


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.adjacent = {}  # key: Node Object, value: weight
        self.distance = sys.maxsize
        self.visited = False
        self.obstacle = False
        self.previous = None

    def add_neighbor(self, neighbor, weight: int = 0) -> None:
        self.adjacent[neighbor] = weight

    def get_distance(self):
        pass

    def set_previous(self, previous):
        pass

    def get_previous(self):
        pass

    def set_visited(self):
        self.visited = True

    def get_visited(self):
        return self.visited

    def set_obstacle(self, obstacle: bool = True):
        self.obstacle = obstacle

    def is_obstacle(self):
        return self.obstacle

    def get_coordinate(self) -> str:
        return f'({self.x}, {self.y})'

    def __eq__(self, other: Node):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Position:({str(self.x)}, {str(self.y)})' \
               f', Distance: {str(self.distance)}' \
               f', {"Obstacle" if self.obstacle else "Open"}'
