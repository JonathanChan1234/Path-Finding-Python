from __future__ import annotations

import sys
from algorithm.Node import Node


class DijkstraNode(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y)
        self.distance = sys.maxsize

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self) -> int:
        return self.distance

    def set_previous(self, previous: DijkstraNode):
        self.previous = previous

    def get_previous(self) -> DijkstraNode:
        return self.previous

    def __str__(self):
        return f'Position:({str(self.x)}, {str(self.y)})' \
               f', Distance: {str(self.distance)}' \
               f', {"Obstacle" if self.obstacle else "Open"}'
