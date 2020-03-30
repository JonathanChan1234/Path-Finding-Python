import pygame
from typing import List, Callable, Tuple
from ui.PathFindingNode import Node

NODE_WIDTH = 20
NODE_HEIGHT = 20
X_OFFSET = 50
Y_OFFSET = 50
BORDER = 2
NODE_COLOR = (50, 129, 168)
BORDER_COLOR = (0, 0, 0)


class Grid:
    def __init__(self,
                 column: int = 20,
                 row: int = 20,
                 color: Tuple[int, int, int] = (50, 129, 168),
                 x_offset: int = X_OFFSET,
                 y_offset: int = Y_OFFSET,
                 width: int = NODE_WIDTH,
                 height: int = NODE_HEIGHT):
        self.grid: List[List[Node]] = []
        self.keydown = False
        self.select_point_mode = False
        self.points: List[Node] = []
        # initialize all the nodes
        for y in range(row):
            self.grid.append([])
            for x in range(column):
                node = Node(width,
                            height,
                            color,
                            BORDER,
                            BORDER_COLOR,
                            x * width + x_offset + BORDER,
                            y * height + y_offset + BORDER,
                            x,
                            y)
                self.grid[y].append(node)

    def grid_iterator(self, func: Callable[[Node], None]):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                func(self.grid[row][column])

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in self.grid:
                for node in row:
                    if node.block_rect.collidepoint(pygame.mouse.get_pos()):
                        if not self.select_point_mode:
                            # if the selected node is already an obstacle, deselected the current cell
                            if node.selected:
                                node.set_selected(False)
                            # if the selected node is NOT an obstacle and not yet make the first click
                            elif not node.selected and not self.keydown:
                                self.keydown = True
                            # if the selected node is NOT yet an obstacle and already make the first click
                            elif not node.selected and \
                                    self.keydown:
                                node.set_selected(True)
                        else:
                            if not node.selected and not node.marked:
                                # set the current point to be origin/destination
                                if len(self.points) == 2:  # remove the last items
                                    self.points.pop(0).set_marked(False)
                                self.points.append(node)
                                node.set_marked(True)

        if event.type == pygame.MOUSEBUTTONUP:
            self.keydown = False

    def clear_all_obstacle(self):
        self.grid_iterator(lambda node: node.set_selected(False))

    def switch_mode(self):
        self.select_point_mode = not self.select_point_mode

    def render(self, window_surface):
        self.grid_iterator(lambda node: Grid.render_node(node, window_surface, self.keydown))

    @staticmethod
    def render_node(node, window_surface, keydown):
        node.render(window_surface)
        if keydown and node.block_rect.collidepoint(pygame.mouse.get_pos()):
            node.set_selected(True)
