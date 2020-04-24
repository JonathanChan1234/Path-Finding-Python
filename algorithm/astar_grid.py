import copy
import math
from typing import List, Union

from algorithm.AStarNode import AStarNode
from algorithm.PriorityHeapQueue import PriorityHeapQueue

VERTICAL_DISTANCE = 1
HORIZONTAL_DISTANCE = 1
DIAGONAL_DISTANCE = 1.4  # sqrt(2)

A_STAR = 'A*'


# check whether it is the valid block (inside the grid and not an obstacle)
def check_valid_block(x: int, y: int, grid: List[List[AStarNode]]):
    if 0 <= y < len(grid) and 0 <= x < len(grid[y]) and not grid[y][x].is_obstacle():
        return True
    return False


def update_node_distance(compared_node: AStarNode, current_node: AStarNode, destination: AStarNode,
                         weight: Union[int, float]):
    if compared_node.get_visited():
        return
    new_g = current_node.get_g() + weight
    new_h = euclidean_distance(compared_node, destination)
    new_distance = new_g + new_h
    if compared_node.get_distance() >= new_distance:
        compared_node.set_previous(current_node)
        compared_node.set_g(new_g)
        compared_node.set_h(new_h)


def euclidean_distance(point1, point2):
    return math.sqrt(math.pow(point1.x - point2.x, 2) + math.pow(point1.y - point2.y, 2))


def comparator(self: AStarNode, other: AStarNode):
    return self.get_distance() - other.get_distance()


def a_star(grid_ref: List[List[AStarNode]],
           origin_ref: AStarNode,
           destination_ref: AStarNode):
    grid = copy.deepcopy(grid_ref)
    origin = grid[origin_ref.y][origin_ref.x]
    destination = grid[destination_ref.y][destination_ref.x]
    origin.set_g(0)
    origin.set_h(0)

    # initialize the priority queue
    unvisited_list = PriorityHeapQueue([], comparator)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if check_valid_block(x, y, grid):
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
    search_result: List[List[List[AStarNode]]] = []

    # if unvisited list is not empty and the destination node is not visited yet
    while not unvisited_list.is_empty() and not destination.get_visited():
        current_node = unvisited_list.pop()
        current_node.set_visited()
        print(f'Current Node {str(current_node)}:')
        for neighbor in neighbors:
            neighbor_x = current_node.x + neighbor['coordinate'][0]
            neighbor_y = current_node.y + neighbor['coordinate'][1]
            if check_valid_block(neighbor_x, neighbor_y, grid):
                update_node_distance(grid[neighbor_y][neighbor_x],
                                     current_node,
                                     destination,
                                     neighbor['distance'])
        search_result.append(copy.deepcopy(grid))

    path_found = destination.get_visited()
    return path_found, search_result


def astar_test() -> float:
    # initialize the test grid
    ROW = 6
    COLUMN = 11
    grid: List[List[AStarNode]] = []
    for y in range(ROW):
        grid.append([])
        for x in range(COLUMN):
            node = AStarNode(x, y)
            grid[y].append(node)

    grid[1][3].set_obstacle(True)
    grid[2][3].set_obstacle(True)
    grid[2][4].set_obstacle(True)
    grid[2][5].set_obstacle(True)
    grid[2][6].set_obstacle(True)
    grid[2][7].set_obstacle(True)


    # astar
    destination = grid[1][4]
    origin = grid[4][7]
    success, search_result = a_star(grid, origin, destination)
    print(f"Path Finding Success: {success}")

    final_result = search_result[len(search_result) - 1]
    # find the path first
    path: List[AStarNode] = []
    next_point = final_result[1][4]
    while next_point.get_previous() is not None:
        next_point = next_point.get_previous()
        path.append(next_point)

    for row in final_result:
        for node in row:
            if origin == node:
                print("o", end='')
            elif destination == node:
                print("x", end='')
            elif node in path:
                print('<>', end='')
            elif node.is_obstacle():
                print('$', end='')
            else:
                print('@', end='')
            print(node.distance_debug(), end='')
        print('')
    return destination.get_distance()


if __name__ == '__main__':
    # print(timeit.timeit(lambda: astar_test(), number=10))
    print(astar_test())
    # after = datetime.now()
    # copy result: 2.1418863999999997
    # deep copy (override __deepcopy__) result: 105.8156528/19.521769799999998
    # deep copy (do not override) result: 413.8303631/68.8988473
