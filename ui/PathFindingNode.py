import math
import os
import sys
from enum import Enum

import pygame
from typing import Tuple

from algorithm.AStarNode import AStarNode

UNVISITED_COLOR = (50, 129, 168)
OBSTACLE_COLOR = (255, 255, 0)
VISITED_COLOR = (255, 0, 0)
SEARCHED_COLOR = (168, 50, 143)
PATH_COLOR = (0, 0, 255)
MARKER_COLOR = (245, 120, 66)
BORDER_COLOR = (0, 0, 0)


class PathFindingNodeState(Enum):
    UNVISITED = 1
    SEARCHED = 2
    OBSTACLE = 3
    VISITED = 4  # shortest path to this node is found
    PATH = 5


class PathFindingNode(pygame.sprite.Sprite, AStarNode):
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
        AStarNode.__init__(self, x, y)

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

        window_surface.blit(self.border, self.border_rect)
        window_surface.blit(self.block, self.block_rect)

        # distance = 'inf' if self.get_distance() == sys.maxsize else str(round(self.get_distance(), 1))
        # g_distance = 'inf' if self.get_g() == sys.maxsize / 2 else str(round(self.get_g(), 1))
        # h_distance = 'inf' if self.get_h() == sys.maxsize / 2 else str(round(self.get_h(), 1))
        #
        # top = self.border_rect.top
        # left = self.border_rect.left
        # right = self.border_rect.right
        # bottom = self.border_rect.bottom
        # centerx = self.border_rect.centerx
        #
        # if g_distance != 'inf':
        #     g_distance_text = pygame.font.SysFont(None, 16).render(g_distance, True, (255, 255, 255))
        #     window_surface.blit(g_distance_text,
        #                         (left + 5, top + 5))
        # if h_distance != 'inf':
        #     h_distance_text = pygame.font.SysFont(None, 16).render(h_distance, True, (0, 0, 0))
        #     h_distance_width = h_distance_text.get_width()
        #     window_surface.blit(h_distance_text,
        #                         (right - h_distance_width - 5, top + 5))
        #
        # if distance != 'inf':
        #     distance_text = pygame.font.SysFont(None, 18).render(distance, True, (0, 100, 255))
        #     distance_width, distance_height = distance_text.get_size()
        #     window_surface.blit(distance_text,
        #                         (centerx - (distance_width / 2), bottom - distance_height - 5))
