from __future__ import annotations

import math
import os
import sys

import pygame
from typing import Tuple, Union, List

from algorithm.Node import Node
from ui_utility.utils import render_inline_text, render_multiline_text

UNVISITED_COLOR = (50, 129, 168)
OBSTACLE_COLOR = (255, 255, 0)
VISITED_COLOR = (255, 0, 0)
SEARCHED_COLOR = (168, 50, 143)
PATH_COLOR = (0, 0, 255)
MARKER_COLOR = (245, 120, 66)
BORDER_COLOR = (0, 0, 0)


class PathFindingNode(pygame.sprite.Sprite, Node):
    def __init__(self,
                 width: int,
                 height: int,
                 border_width: int,
                 x_pos: int,
                 y_pos: int,
                 x: int,
                 y: int):
        # constructor
        pygame.sprite.Sprite.__init__(self)
        Node.__init__(self, x, y)

        # node properties
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos

        # node border properties
        self.border_width = border_width

        # node block
        self.block = pygame.Surface([self.width, self.height])
        self.block.fill(UNVISITED_COLOR)
        self.block_rect = self.block.get_rect()
        self.block_rect.topleft = (x_pos + self.border_width, y_pos + self.border_width)

        # node block border
        self.border = pygame.Surface([self.width + self.border_width * 2, self.height + self.border_width * 2])
        self.border.fill(BORDER_COLOR)
        self.border_rect = self.border.get_rect()
        self.border_rect.topleft = (x_pos, y_pos)

        # coordinate
        self.x = x
        self.y = y

        # other properties
        self.marked = False
        self.is_path = False
        self.debug_text: Union[str, List[str]] = ''
        self.debug_mode = False

        # marker
        # set marker to the middle of the node block
        marker_image = pygame.image.load(os.path.join(os.getcwd(), '../asset/marker.png'))
        self.marker = pygame.transform.scale(marker_image, (math.floor(width), math.floor(height)))
        self.marker_rect = self.marker.get_rect()
        block_width, block_height = self.block.get_size()
        x_offset = (self.width - block_width) / 2
        y_offset = (self.height - block_height) / 2
        self.marker_rect.topleft = (x_pos + x_offset, y_pos + y_offset)

    def set_marked(self, marked: bool):
        self.marked = marked

    def is_marked(self) -> bool:
        return self.marked

    def set_path(self):
        self.is_path = True

    def set_debug_mode(self, debug_mode):
        self.debug_mode = debug_mode

    def set_debug_text(self, debug_text: str):
        self.debug_text = debug_text

    def check_crash(self, pos: Tuple[int, int]):
        return self.block_rect.collidepoint(pos)

    def render(self, window_surface: pygame.SurfaceType):
        if self.is_obstacle():
            self.block.fill(OBSTACLE_COLOR)
        elif self.marked:
            self.block.fill(MARKER_COLOR)
        elif self.is_path:
            self.block.fill(PATH_COLOR)
        elif self.get_visited():
            self.block.fill(VISITED_COLOR)
        else:
            if self.get_distance() == sys.maxsize:
                self.block.fill(UNVISITED_COLOR)
            else:
                self.block.fill(SEARCHED_COLOR)
        if self.debug_mode:
            if self.get_distance() != sys.maxsize:
                if type(self.debug_text) is list:
                    render_multiline_text(self.block, self.debug_text, 8, (0, 0, 0))
                if type(self.debug_text) == str:
                    render_inline_text(self.block, self.debug_text, 8, (0, 0, 0))
        window_surface.blit(self.border, self.border_rect)
        window_surface.blit(self.block, self.block_rect)

    def set_previous(self, previous: PathFindingNode):
        self.previous = previous

    def get_previous(self) -> PathFindingNode:
        return self.previous
