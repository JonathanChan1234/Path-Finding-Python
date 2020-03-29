import pygame
from typing import Tuple

SELECTED_COLOR = (255, 255, 0)


class Node(pygame.sprite.Sprite):
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
        super().__init__()
        self.width = width
        self.height = height
        # node block
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
        self.selected = False

    def set_selected(self, selected: bool):
        self.selected = selected
        if self.selected:
            self.block.fill(SELECTED_COLOR)
        else:
            self.block.fill(self.color)

    def get_coordinate(self):
        return self.x, self.y

    def update(self):
        print("Path Finding Node is updating")
