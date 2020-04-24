import copy
import sys
from typing import List, Union
from algorithm.DijkstraNode import DijkstraNode
from algorithm.Node import Node
from algorithm.PriorityHeapQueue import PriorityHeapQueue
from ui.PathFindingNode import PathFindingNode

ROW = 10
COLUMN = 10
VERTICAL_DISTANCE = 1
HORIZONTAL_DISTANCE = 1
DIAGONAL_DISTANCE = 1.4  # sqrt(2)
DIJKSTRA = "Dijkstra"


def debug_grid(grid: List[List[DijkstraNode]]):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(grid[y][x])


def debug_shortest_path(grid: List[List[DijkstraNode]], origin: DijkstraNode, destination: DijkstraNode) -> float:
    # find the path first
    path: List[DijkstraNode] = []
    next_point = destination
    while next_point.get_previous() is not None:
        next_point = next_point.get_previous()
        path.append(next_point)

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if origin == grid[y][x]:
                print("o", end='')
            elif destination == grid[y][x]:
                print("x", end='')
            elif grid[y][x] in path:
                print(' ', end='')
            elif grid[y][x].is_obstacle():
                print('$', end='')
            else:
                print('@', end='')
        print('')
    return destination.get_distance()


def init_grid(grid: List[List[DijkstraNode]], row: int, column: int):
    for y in range(row):
        grid.append([])
        for x in range(column):
            grid[y].append(DijkstraNode(x, y))


def update_node_distance(compared_node: DijkstraNode, current_node: DijkstraNode, weight: Union[int, float]):
    if not compared_node.get_visited():
        new_distance = current_node.get_distance() + weight
        if compared_node.get_distance() > new_distance:
            compared_node.set_previous(current_node)
            compared_node.set_distance(new_distance)


def check_valid_block(x: int, y: int, grid: List[List[DijkstraNode]]) -> bool:
    # Check the node is inside the grid and not an obstacle
    if 0 <= y < len(grid) and 0 <= x < len(grid[y]) and not grid[y][x].is_obstacle():
        return True
    return False


def comparator(self: DijkstraNode, other: DijkstraNode):
    return self.get_distance() - other.get_distance()


def copy_grid(grid: List[List[Node]]) -> List[List[DijkstraNode]]:
    new_grid: List[List[DijkstraNode]] = []
    for row in range(len(grid)):
        new_grid_row = []
        for column in range(len(grid[row])):
            new_grid_row.append(DijkstraNode(grid[row][column].x, grid[row][column].y))
        new_grid.append(new_grid_row)
    return new_grid


def copy_immediate_result(immediate_result: List[List[DijkstraNode]], grid: List[List[PathFindingNode]]):
    animation = copy.deepcopy(grid)
    for row in range(len(immediate_result)):
        for column in range(len(immediate_result[row])):
            if immediate_result[row][column].get_distance() != sys.maxsize:
                animation[row][column].distance = immediate_result[row][column].get_distance()
                if immediate_result[row][column].get_visited():
                    animation[row][column].set_visited()
                if immediate_result[row][column].get_previous():
                    previous_node = immediate_result[row][column].get_previous()
                    print(f'previous_node of node {column, row} is {previous_node}')
                    animation[row][column].set_previous(animation[previous_node.y][previous_node.x])
    return animation


def dijkstra(grid: List[List[PathFindingNode]], origin: PathFindingNode, destination: PathFindingNode):
    dijkstra_grid = copy_grid(grid)
    dijkstra_grid_origin = dijkstra_grid[origin.y][origin.x]
    dijkstra_grid_destination = dijkstra_grid[destination.y][destination.x]

    # create a copy of Dijkstra Node with the same attribute as grid
    # set the distance of the origin to 0
    dijkstra_grid_origin.set_distance(0)

    # create an unvisited vertex list
    # push all the node other than the origin to the list
    unvisited_list = PriorityHeapQueue([], comparator)
    for nodeList in dijkstra_grid:
        for node in nodeList:
            if not node.is_obstacle():
                unvisited_list.insert(node)

    neighbors = [
        {'distance': VERTICAL_DISTANCE, 'coordinate': [0, -1]},
        {'distance': HORIZONTAL_DISTANCE, 'coordinate': [-1, 0]},
        {'distance': HORIZONTAL_DISTANCE, 'coordinate': [1, 0]},
        {'distance': VERTICAL_DISTANCE, 'coordinate': [0, 1]},
        {'distance': DIAGONAL_DISTANCE, 'coordinate': [-1, -1]},
        {'distance': DIAGONAL_DISTANCE, 'coordinate': [1, -1]},
        {'distance': DIAGONAL_DISTANCE, 'coordinate': [-1, 1]},
        {'distance': DIAGONAL_DISTANCE, 'coordinate': [1, 1]}
    ]
    animation: List[List[List[PathFindingNode]]] = []

    while not unvisited_list.is_empty() and not dijkstra_grid_destination.get_visited():
        # Find the nearest node first (node with the smallest distance)
        current_node = unvisited_list.pop()

        # Set the current node to be "visited"
        current_node.set_visited()

        for neighbor in neighbors:
            neighbor_x = current_node.x + neighbor['coordinate'][0]
            neighbor_y = current_node.y + neighbor['coordinate'][1]

            if check_valid_block(neighbor_x, neighbor_y, dijkstra_grid):
                update_node_distance(dijkstra_grid[neighbor_y][neighbor_x],
                                     current_node,
                                     neighbor['distance'])
        animation.append(copy_immediate_result(dijkstra_grid, grid))

    path_found = dijkstra_grid_destination.get_visited()
    return path_found, animation
