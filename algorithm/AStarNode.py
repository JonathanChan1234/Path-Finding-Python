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
        if self.g == sys.maxsize / 2 and self.h == sys.maxsize / 2:
            return sys.maxsize
        return self.g + self.h

    def debug_text(self):
        if self.get_distance() == sys.maxsize:
            return ''
        else:
            return [f'g: {round(self.get_g(), 2)}',
                    f'h: {round(self.get_h(), 2)}',
                    f'f: {round(self.get_distance(), 2)}']
