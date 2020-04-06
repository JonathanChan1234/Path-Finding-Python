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
        self.state: PathFindingNodeState = PathFindingNodeState.UNVISITED

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
        self.state = PathFindingNodeState.PATH

    def check_crash(self, pos: Tuple[int, int]):
        return self.block_rect.collidepoint(pos)

    def set_g(self, g):
        AStarNode.set_g(self, g)
        if self.get_distance() != sys.maxsize:
            self.state = PathFindingNodeState.SEARCHED

    def set_h(self, h):
        AStarNode.set_h(self, h)
        if self.get_distance() != sys.maxsize:
            self.state = PathFindingNodeState.SEARCHED

    def set_visited(self):
        AStarNode.set_visited(self)
        self.state = PathFindingNodeState.VISITED

    def set_obstacle(self, obstacle: bool = True):
        AStarNode.set_obstacle(self, obstacle)
        self.state = PathFindingNodeState.OBSTACLE if obstacle else PathFindingNodeState.UNVISITED

    def render(self, window_surface: pygame.SurfaceType):
        if self.state == PathFindingNodeState.UNVISITED:
            self.block.fill(UNVISITED_COLOR)
        elif self.state == PathFindingNodeState.OBSTACLE:
            self.block.fill(OBSTACLE_COLOR)
        elif self.state == PathFindingNodeState.VISITED:
            self.block.fill(VISITED_COLOR)
        elif self.state == PathFindingNodeState.SEARCHED:
            self.block.fill(SEARCHED_COLOR)
        elif self.state == PathFindingNodeState.PATH:
            self.block.fill(PATH_COLOR)

        window_surface.blit(self.border, self.border_rect)
        window_surface.blit(self.block, self.block_rect)
        if self.marked:
            window_surface.blit(self.marker, self.marker_rect)
