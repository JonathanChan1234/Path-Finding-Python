import sys

import pygame
from typing import List, Tuple

from algorithm.astar_grid import a_star
from ui.PathFindingNode import PathFindingNode

NODE_WIDTH = 20
NODE_HEIGHT = 20
X_OFFSET = 50
Y_OFFSET = 50
BORDER = 2
NODE_COLOR = (50, 129, 168)
BORDER_COLOR = (0, 0, 0)


class PathFindingGrid:
    VERTICAL_DISTANCE = 1
    HORIZONTAL_DISTANCE = 1
    DIAGONAL_DISTANCE = 1.4  # sqrt(2)
    PATH_FIND_ID = pygame.NUMEVENTS - 1

    def __init__(self,
                 column: int = 20,
                 row: int = 20,
                 color: Tuple[int, int, int] = NODE_COLOR,
                 x_offset: int = X_OFFSET,
                 y_offset: int = Y_OFFSET,
                 width: int = NODE_WIDTH,
                 height: int = NODE_HEIGHT):
        self.grid: List[List[PathFindingNode]] = []

        self.keydown = False
        self.select_point_mode = False
        self.markers: List[PathFindingNode] = []
        self.path_find_animation_started = False
        self.search_result: List[List[List[PathFindingNode]]] = []

        # initialize all the nodes
        for y in range(row):
            self.grid.append([])
            for x in range(column):
                node = PathFindingNode(width,
                                       height,
                                       color,
                                       BORDER,
                                       BORDER_COLOR,
                                       x * width + x_offset + BORDER,
                                       y * height + y_offset + BORDER,
                                       x,
                                       y)
                self.grid[y].append(node)

    def grid_iterator(self, func):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                func(self.grid[row][column])

    def event_handler(self, event):
        if event.type == PathFindingGrid.PATH_FIND_ID:
            self.update_grid()
        if self.path_find_animation_started:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            self.keydown = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in self.grid:
                for node in row:
                    if node.check_crash(pygame.mouse.get_pos()):
                        if self.select_point_mode:
                            self.set_marker(node)
                        else:
                            self.set_obstacle(node)

    def set_obstacle(self, node):
        # if the selected node is already an obstacle, deselected the current cell
        if node.is_obstacle():
            node.set_obstacle(False)
        # if the selected node is NOT an obstacle and not yet make the first click
        elif not node.is_obstacle() and not self.keydown:
            self.keydown = True
            node.set_obstacle(True)

    def set_marker(self, node):
        if not node.is_obstacle() and not node.is_marked():
            # set the current point to be origin/destination
            if len(self.markers) == 2:  # remove the last items
                self.markers.pop(0).set_marked(False)
            self.markers.append(node)
            node.set_marked(True)

    def clear_all_obstacle(self):
        self.grid_iterator(lambda node: node.set_obstacle(False))

    def is_marker_set(self):
        return len(self.markers) == 2

    def switch_mode(self):
        self.select_point_mode = not self.select_point_mode

    def set_animation_started(self, started: bool):
        self.path_find_animation_started = started

    def start_path_find(self):
        if len(self.markers) != 2:
            raise Exception("Missing Origin/Destination Point")
        self.set_animation_started(True)
        origin, destination = self.markers[0], self.markers[1]
        pygame.time.delay(2000)
        self.search_result = a_star(self.grid, origin, destination)
        pygame.time.set_timer(PathFindingGrid.PATH_FIND_ID, 10)

    def update_grid(self):
        # ignore the event counter when the animation is finished
        if len(self.search_result) == 0:
            return

        print('update grid')
        # draw the immediate result (animation)
        search_result_history = self.search_result.pop(0)
        for row in range(len(search_result_history)):
            for column in range(len(search_result_history[row])):
                self.grid[row][column].set_g(search_result_history[row][column].get_g())
                self.grid[row][column].set_h(search_result_history[row][column].get_h())
                if search_result_history[row][column].get_previous():
                    previous_node = search_result_history[row][column].get_previous()
                    print(previous_node.get_coordinate())
                    self.grid[row][column].set_previous(self.grid[previous_node.y][previous_node.x])

        # draw the final path
        if len(self.search_result) == 0:
            next_point = self.markers[1]
            while next_point.get_previous() is not None:
                next_point.set_path(True)
                next_point = next_point.get_previous()
            self.set_animation_started(False)

    def render(self, window_surface):
        self.grid_iterator(lambda node: self.render_node(node, window_surface))

    def render_node(self, node, window_surface):
        node.render(window_surface)
        if self.path_find_animation_started:
            return
        # Set the node that the player currently hover when these 3 conditions is fulfilled
        # 1. The player has made the first (initial click)
        # 2. The hover position is within a valid node
        # 3. The node is currently NOT marked
        if self.keydown \
                and node.check_crash(pygame.mouse.get_pos()) \
                and not node.is_marked():
            node.set_obstacle(True)
