import copy
import math
from datetime import datetime
from typing import List, Union
import timeit

import pygame

from ui.PathFindingNode import PathFindingNode
from algorithm.PriorityQueue import PriorityQueue

VERTICAL_DISTANCE = 1
HORIZONTAL_DISTANCE = 1
DIAGONAL_DISTANCE = 1.4  # sqrt(2)


# check whether it is the valid block (inside the grid and not an obstacle)
def check_valid_block(x: int, y: int, grid: List[List[PathFindingNode]]):
    if 0 <= y < len(grid) and 0 <= x < len(grid[y]) and not grid[y][x].is_obstacle():
        return True
    return False


def update_node_distance(compared_node: PathFindingNode, current_node: PathFindingNode, destination: PathFindingNode,
                         weight: Union[int, float]):
    if compared_node.get_visited():
        return
    new_g = current_node.get_distance() + weight
    new_h = euclidean_distance(current_node, destination)
    new_distance = new_g + new_h
    if compared_node.get_distance() >= new_distance:
        compared_node.set_previous(current_node)
        compared_node.set_g(new_g)
        compared_node.set_h(new_h)
        print(f"Updated for the vertex {str(compared_node)}"
              f"(New Distance {new_distance} > Original Distance {compared_node.get_distance()})")
    else:
        print(f"Updated for the vertex {str(compared_node)}"
              f"(New Distance {new_distance} < Original Distance {compared_node.get_distance()})")


def euclidean_distance(point1, point2):
    return math.sqrt(math.pow(point1.x - point2.x, 2) + math.pow(point1.y - point2.y, 2))


def a_star(grid_ref: List[List[PathFindingNode]],
           origin_ref: PathFindingNode,
           destination_ref: PathFindingNode) -> \
        List[List[List[PathFindingNode]]]:
    grid = copy.deepcopy(grid_ref)
    origin = grid[origin_ref.y][origin_ref.x]
    destination = grid[destination_ref.y][destination_ref.x]
    origin.set_g(0)
    origin.set_h(0)

    # initialize the priority queue
    unvisited_list = PriorityQueue()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(type(grid[y][x]))
            unvisited_list.insert(grid[y][x])

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
    search_result: List[List[List[PathFindingNode]]] = []

    # if unvisited list is not empty and the destination node is not visited yet
    while not unvisited_list.is_empty() and not destination.get_visited():
        # the first current node should be the origin
        x, y = unvisited_list.pop()
        current_node = grid[y][x]
        print(f'Current PathFindingNode {str(current_node)}:')
        for neighbor in neighbors:
            neighbor_x = current_node.x + neighbor['coordinate'][0]
            neighbor_y = current_node.y + neighbor['coordinate'][1]
            if check_valid_block(neighbor_x, neighbor_y, grid):
                update_node_distance(grid[neighbor_y][neighbor_x],
                                     current_node,
                                     destination,
                                     neighbor['distance'])
        search_result.append(copy.deepcopy(grid))
        current_node.set_visited()
    return search_result


def astar_test() -> float:
    # initialize the test grid
    ROW = 20
    COLUMN = 20
    grid: List[List[PathFindingNode]] = []
    for y in range(ROW):
        grid.append([])
        for x in range(COLUMN):
            node = PathFindingNode(20,
                                   20,
                                   (50, 129, 168),
                                   2,
                                   (0, 0, 0),
                                   x * 20 + 50 + 5,
                                   y * 20 + 50 + 5,
                                   x,
                                   y)
            grid[y].append(node)

    for row in range(ROW):
        grid[row][row].set_obstacle()

    # astar
    origin = grid[0][0]
    destination = grid[9][8]
    search_result = a_star(grid, origin, destination)
    print(len(search_result))

    # find the path first
    path: List[PathFindingNode] = []
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
            # print(grid[y][x].distance_debug(), end='')
        print('')
    return destination.get_distance()


if __name__ == '__main__':
    # print(timeit.timeit(lambda: astar_test(), number=10))
    print(astar_test())
    after = datetime.now()
    # copy result: 2.1418863999999997
    # deep copy (override __deepcopy__) result: 105.8156528/19.521769799999998
    # deep copy (do not override) result: 413.8303631/68.8988473
