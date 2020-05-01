import math
from random import randint
from typing import List, Tuple


class MazeNode:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.obstacle: bool = False
        self.visited: bool = False

    def is_obstacle(self) -> bool:
        return self.obstacle

    def is_visited(self) -> bool:
        return self.visited

    def set_obstacle(self):
        self.obstacle = True

    def break_obstacle(self):
        self.obstacle = False

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return f'({self.x}, {self.y})'


class MazeGrid:
    neighbors = [[0, 2], [0, -2], [2, 0], [-2, 0]]

    def __init__(self, row: int, column: int):
        self.row: int = row
        self.column: int = column
        self.grid: List[List[MazeNode]] = []
        self.init_grid()

    def init_grid(self):
        for y in range(self.row):
            row = []
            for x in range(self.column):
                node = MazeNode(x, y)
                if x % 2 != 0 or y % 2 != 0:
                    node.set_obstacle()
                row.append(node)
            self.grid.append(row)

    def get_node(self, x, y) -> MazeNode:
        return self.grid[y][x]

    def is_node_valid(self, x: int, y: int):
        return 0 <= x < self.column and 0 <= y < self.row

    def is_node_visited(self, x: int, y: int) -> bool:
        return self.grid[y][x].is_visited()

    def get_neighbor_nodes(self, x: int, y: int) -> List[MazeNode]:
        """
        get all the valid and unvisited neighbor nodes of the node with coordinate x and y
        :param x: x coordinate of the node
        :param y: y coordinate of the node
        :return: list of neighbor nodes , empty list if there is no neighbor nodes
        """
        node_neighbors = []
        for neighbor in MazeGrid.neighbors:
            if self.is_node_valid(x + neighbor[0], y + neighbor[1]):
                if not self.is_node_visited(x + neighbor[0], y + neighbor[1]):
                    node_neighbors.append(self.get_node(x + neighbor[0], y + neighbor[1]))
        return node_neighbors

    def mark_node_visited(self, x: int, y: int):
        self.grid[y][x].set_visited()

    def break_node_wall(self, x: int, y: int, other_x: int, other_y: int):
        # right
        if other_x - x == 2:
            self.grid[y][x + 1].break_obstacle()
        # left
        if other_x - x == -2:
            self.grid[y][x - 1].break_obstacle()
        # bottom
        if other_y - y == 2:
            self.grid[y + 1][x].break_obstacle()
        # top
        if other_y -y == -2:
            self.grid[y - 1][x].break_obstacle()

    def get_all_obstacle(self) -> List[Tuple[int, int]]:
        obstacle_list: List[Tuple[int, int]] = []
        for row in self.grid:
            for node in row:
                if node.is_obstacle():
                    obstacle_list.append((node.x, node.y))
        return obstacle_list

    def grid_debug(self):
        for row in self.grid:
            for node in row:
                if node.is_obstacle():
                    print('*', end='')
                else:
                    print('-', end='')
            print('')


def maze_generation(grid: MazeGrid):
    # pick a random node
    current_x, current_y = randint(0, math.floor(grid.column / 2)) * 2, randint(0, math.floor(grid.row / 2)) * 2
    depth_list: List[Tuple[int, int]] = [(current_x, current_y)]

    while len(depth_list) > 0:
        neighbor_nodes = grid.get_neighbor_nodes(current_x, current_y)
        if len(neighbor_nodes) > 0:
            # select a random neighboring node that has not been visited yet
            random_neighbor = neighbor_nodes[randint(0, len(neighbor_nodes) - 1)]

            # break the wall between these two nodes
            grid.break_node_wall(current_x, current_y, random_neighbor.x, random_neighbor.y)

            # push the current node to the stack
            depth_list.append((random_neighbor.x, random_neighbor.y))

            # mark the current node as visited
            grid.mark_node_visited(current_x, current_y)
            grid.mark_node_visited(random_neighbor.x, random_neighbor.y)

            # marked as current node
            current_x, current_y = random_neighbor.x, random_neighbor.y
        else:
            current_x, current_y = depth_list.pop(0)
    return grid.get_all_obstacle()


def dfs_maze_generation(grid):
    # create a copy of the grid
    maze_grid = MazeGrid(column=grid.column, row=grid.row)

    # maze generation
    return maze_generation(maze_grid)
