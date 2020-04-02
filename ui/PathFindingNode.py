import math
import os
import sys

import pygame
from typing import Tuple

from algorithm.AStarNode import AStarNode

SELECTED_COLOR = (255, 255, 0)
VISITED_COLOR = (255, 0, 0)
PATH_COLOR = (0, 0, 255)


class PathFindingNode(pygame.sprite.Sprite, AStarNode):
    def __init__(self,
                 width: int,
                 height: int,
                 color: Tuple[int, int, int],
                 border_width: int,
                 border_color: Tuple[int, int, int],
                 x_pos: int,
                 y_pos: int,
                 x: int,
                 y: int):
        # constructor
        pygame.sprite.Sprite.__init__(self)
        AStarNode.__init__(self, x, y)

        # node properties
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos

        # node border properties
        self.border_width = border_width
        self.border_color = border_color

        # node block
        self.block = pygame.Surface([self.width, self.height])
        self.block.fill(color)
        self.block_rect = self.block.get_rect()
        self.block_rect.topleft = (x_pos + self.border_width, y_pos + self.border_width)

        # node block border
        self.border = pygame.Surface([self.width + self.border_width * 2, self.height + self.border_width * 2])
        self.border.fill(border_color)
        self.border_rect = self.border.get_rect()
        self.border_rect.topleft = (x_pos, y_pos)

        # coordinate
        self.x = x
        self.y = y

        # other properties
        self.color = color
        self.marked = False
        self.searched = False
        self.is_path = False

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

    def set_searched(self, searched: bool):
        self.searched = searched

    def is_searched(self) -> bool:
        return self.searched

    def set_path(self, path: bool):
        self.is_path = path

    def get_path(self) -> bool:
        return self.is_path

    def check_crash(self, pos: Tuple[int, int]):
        return self.block_rect.collidepoint(pos)

    def render(self, window_surface: pygame.SurfaceType):
        if self.obstacle:
            self.block.fill(SELECTED_COLOR)
        elif self.get_distance() != sys.maxsize:
            self.block.fill(VISITED_COLOR)
        else:
            self.block.fill(self.color)

        if self.get_path():
            self.block.fill(PATH_COLOR)
        window_surface.blit(self.border, self.border_rect)
        window_surface.blit(self.block, self.block_rect)
        if self.marked:
            window_surface.blit(self.marker, self.marker_rect)

    def __deepcopy__(self, memodict={}):
        copy_node = PathFindingNode(self.width, self.height, self.color, self.border_width, self.border_color,
                                    self.x_pos, self.y_pos, self.x, self.y)
        copy_node.g = self.g
        copy_node.h = self.h
        copy_node.obstacle = self.obstacle
        copy_node.visited = self.visited
        copy_node.previous = self.previous
        copy_node.marked = self.marked
        copy_node.searched = self.searched
        return copy_node
