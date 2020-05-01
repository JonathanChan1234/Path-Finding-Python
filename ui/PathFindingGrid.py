import pygame
from typing import List, Tuple

from algorithm.PathFindingState import PathFindingState
from algorithm.astar_grid import A_STAR, a_star
from algorithm.dfs_maze import dfs_maze_generation
from algorithm.dijkstra_grid import dijkstra, DIJKSTRA
from ui.PathFindingNode import PathFindingNode

NODE_WIDTH = 50
NODE_HEIGHT = 50
X_OFFSET = 50
Y_OFFSET = 50
BORDER = 2
NODE_COLOR = (50, 129, 168)
BORDER_COLOR = (0, 0, 0)


class PathFindingGrid:
    PATH_ANIMATION_ID = pygame.NUMEVENTS - 1

    def __init__(self,
                 algorithm: str,
                 column: int = 20,
                 row: int = 20,
                 color: Tuple[int, int, int] = NODE_COLOR,
                 x_offset: int = X_OFFSET,
                 y_offset: int = Y_OFFSET,
                 width: int = NODE_WIDTH,
                 height: int = NODE_HEIGHT,
                 border_width: int = BORDER):
        # Selected Path Finding Algorithm
        self.algorithm = algorithm

        # True when the player has made the first initial click, the hovered block will become obstacle
        self.select_obstacle = False

        # True when the player is currently in selecting the origin/destination
        self.select_marker = False

        # Debug mode
        self.debug_mode = False

        self.disabled = False
        self.path_find_finished = False
        self.markers: List[PathFindingNode] = []
        self.search_result: List[List[List[PathFindingState]]] = []

        self.grid: List[List[PathFindingNode]] = []
        self.column = column
        self.row = row
        self.color = color
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.border_width = border_width
        self.init_grid()

    def init_grid(self):
        self.grid.clear()
        for row in range(self.row):
            grid_row = []
            for column in range(self.column):
                node = PathFindingNode(self.width,
                                       self.height,
                                       BORDER,
                                       column * self.width + self.x_offset + self.border_width,
                                       row * self.height + self.y_offset + self.border_width,
                                       column,
                                       row)
                grid_row.append(node)
            self.grid.append(grid_row)

    def grid_iterator(self, func):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                func(self.grid[row][column])

    def set_algorithm(self, algorithm: str):
        self.algorithm = algorithm

    def set_obstacle(self, node):
        # if the selected node is already an obstacle, deselected the current cell
        if node.is_obstacle():
            node.set_obstacle(False)
        # if the selected node is NOT an obstacle and not yet make the first click
        elif not node.is_obstacle() and not self.select_obstacle:
            self.select_obstacle = True
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
        self.select_marker = not self.select_marker

    def set_disabled(self, disabled: bool):
        self.disabled = disabled

    def is_disabled(self):
        return self.disabled

    def set_path_find_finished(self, finished: bool):
        self.path_find_finished = finished

    def is_path_find_finished(self):
        return self.path_find_finished

    def set_debug_mode(self, debug_mode):
        self.debug_mode = debug_mode
        self.grid_iterator(lambda node: node.set_debug_mode(debug_mode))

    def draw_maze(self):
        self.reset_grid()
        obstacle_list = dfs_maze_generation(self)
        for obstacle in obstacle_list:
            obstacle_x, obstacle_y = obstacle
            self.grid[obstacle_y][obstacle_x].set_obstacle()

    def start_path_find(self):
        if len(self.markers) != 2:
            raise Exception("Missing Origin/Destination Point")
        origin, destination = self.markers[0], self.markers[1]
        if self.algorithm == DIJKSTRA:
            path_found, self.search_result = dijkstra(self.grid, origin, destination)
        elif self.algorithm == A_STAR:
            path_found, self.search_result = a_star(self.grid, origin, destination)
        else:
            print('This algorithm is not implemented yet')
            return
        print(len(self.search_result))
        self.set_disabled(True)
        pygame.time.set_timer(PathFindingGrid.PATH_ANIMATION_ID, 10)

    def update_grid(self):
        # ignore the event counter when the animation is finished
        if len(self.search_result) == 0:
            return

        # update the immediate result to the UI
        immediate_result = self.search_result.pop(0)
        for row in range(len(immediate_result)):
            for column in range(len(immediate_result[row])):
                node_state = immediate_result[row][column]
                if node_state.visited:
                    self.grid[row][column].set_visited()
                if node_state.previous:
                    previous_x, previous_y = node_state.previous
                    self.grid[row][column].set_previous(self.grid[previous_y][previous_x])
                self.grid[row][column].set_distance(node_state.distance)
                self.grid[row][column].set_debug_text(node_state.debug_text)

        # draw the final path
        if len(self.search_result) == 0:
            next_point = self.markers[1]
            while next_point.get_previous():
                next_point.set_path()
                next_point = next_point.get_previous()
            self.set_path_find_finished(True)

    def reset_grid(self):
        self.init_grid()
        self.set_disabled(False)
        self.set_path_find_finished(False)
        self.markers.clear()
        self.search_result.clear()

    def event_handler(self, event):
        if event.type == PathFindingGrid.PATH_ANIMATION_ID and \
                self.disabled:
            self.update_grid()
        if event.type == pygame.MOUSEBUTTONUP and not self.disabled:
            self.select_obstacle = False
        if event.type == pygame.MOUSEBUTTONDOWN and not self.disabled:
            for row in self.grid:
                for node in row:
                    if node.check_crash(pygame.mouse.get_pos()):
                        if self.select_marker:
                            self.set_marker(node)
                        else:
                            self.set_obstacle(node)

    def render(self, window_surface):
        self.grid_iterator(lambda node: self.render_node(node, window_surface))

    def render_node(self, node, window_surface):
        node.render(window_surface)
        if self.disabled:
            return

        # Set the node that the player currently hover when these 3 conditions is fulfilled
        # 1. The player has made the first (initial click)
        # 2. The hover position is within a valid node
        # 3. The node is currently NOT marked
        if self.select_obstacle \
                and node.check_crash(pygame.mouse.get_pos()) \
                and not node.is_marked():
            node.set_obstacle(True)
