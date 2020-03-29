import pygame
from typing import List
from ui.PathFindingNode import Node

NODE_WIDTH = 50
NODE_HEIGHT = 50
X_OFFSET = 20
Y_OFFSET = 20
BORDER = 5
NODE_COLOR = (50, 129, 168)
BORDER_COLOR = (0, 0, 0)


class Grid:
    def __init__(self, column, row):
        self.grid: List[List[Node]] = []
        # initialize all the nodes
        for y in range(row):
            self.grid.append([])
            for x in range(column):
                node = Node(NODE_WIDTH,
                            NODE_HEIGHT,
                            NODE_COLOR,
                            BORDER,
                            BORDER_COLOR,
                            x * NODE_WIDTH + X_OFFSET + BORDER,
                            y * NODE_HEIGHT + Y_OFFSET + BORDER,
                            x,
                            y)
                self.grid[y].append(node)

    def check_selected_block(self, mouse_pos):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.grid[row][column].block_rect.collidepoint(mouse_pos):
                    return self.grid[row][column].selected

    def handle_hover(self, mouse_pos):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.grid[row][column].block_rect.collidepoint(mouse_pos):
                    self.grid[row][column].set_selected(True)

    def deselect_cell(self, mouse_pos):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.grid[row][column].block_rect.collidepoint(mouse_pos):
                    self.grid[row][column].set_selected(False)

    def render(self, window_surface):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                window_surface.blit(self.grid[row][column].border, self.grid[row][column].border_rect)
                window_surface.blit(self.grid[row][column].block, self.grid[row][column].block_rect)
