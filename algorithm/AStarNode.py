from __future__ import annotations

import sys
import math

from algorithm.Node import Node


class AStarNode(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y)
        self.g = sys.maxsize / 2
        self.h = sys.maxsize / 2

    def __str__(self):
        return f'Position: ({self.x}, {self.y}), Distance: {self.g + self.h}'

    def set_previous(self, previous: AStarNode):
        self.previous = previous

    def get_previous(self) -> AStarNode:
        return self.previous

    def set_g(self, g):
        self.g = g

    def get_g(self):
        return self.g

    def set_h(self, h):
        self.h = h

    def get_h(self):
        return self.h

    def get_distance(self) -> int:
        return self.g + self.h

    def distance_debug(self):
        if self.g == sys.maxsize /2 and self.h == sys.maxsize /2:
            return '(inf, inf)'
        else:
            return f'({math.floor(self.g), math.floor(self.h)})'

    def status(self):
        return {
            'g': self.g,
            'h': self.h,
            'visited': self.visited
        }

    def __deepcopy__(self, memodict={}):
        copy_node = AStarNode(self.x, self.y)
        copy_node.g = self.g
        copy_node.h = self.h
        copy_node.obstacle = self.obstacle
        copy_node.visited = self.visited
        copy_node.previous = self.previous
        copy_node.obstacle = self.obstacle
        return copy_node
