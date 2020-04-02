import math
import os

import pygame
from typing import Tuple

from algorithm.AStarNode import AStarNode

SELECTED_COLOR = (255, 255, 0)


class PathFindingNode(pygame.sprite.Sprite, AStarNode):
    def __init__(self,
                 width: int,
                 height: int,
                 color: Tuple[int, int, int],
                 border: int,
                 border_color: Tuple[int, int, int],
                 x_pos: int,
                 y_pos: int,
                 x: int,
                 y: int):
        # constructor
        pygame.sprite.Sprite.__init__(self)
        AStarNode.__init__(self, x, y)

        # node block
        self.width = width
        self.height = height
        self.block = pygame.Surface([self.width, self.height])
        self.block.fill(color)
        self.block_rect = self.block.get_rect()
        self.block_rect.topleft = (x_pos + border, y_pos + border)

        # node block border
        self.border = pygame.Surface([self.width + border * 2, self.height + border * 2])
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

    def is_searched(self):
        return self.searched

    def check_crash(self, pos: Tuple[int, int]):
        return self.block_rect.collidepoint(pos)

    def render(self, window_surface: pygame.SurfaceType):
        if self.obstacle:
            self.block.fill(SELECTED_COLOR)
        else:
            self.block.fill(self.color)
        window_surface.blit(self.border, self.border_rect)
        window_surface.blit(self.block, self.block_rect)
        if self.marked:
            window_surface.blit(self.marker, self.marker_rect)
