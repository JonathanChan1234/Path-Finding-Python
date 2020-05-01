import math
from typing import List, Union

from algorithm.AStarNode import AStarNode
from algorithm.Node import Node
from algorithm.PathFindingState import PathFindingState
from algorithm.PriorityHeapQueue import PriorityHeapQueue
from ui.PathFindingNode import PathFindingNode

VERTICAL_DISTANCE = 1
HORIZONTAL_DISTANCE = 1
DIAGONAL_DISTANCE = 1.4  # sqrt(2)
A_STAR = 'A*'
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


def copy_grid(grid: List[List[Node]]) -> List[List[AStarNode]]:
    new_grid: List[List[AStarNode]] = []
    for row in range(len(grid)):
        new_grid_row = []
        for column in range(len(grid[row])):
            node = AStarNode(grid[row][column].x, grid[row][column].y)
            node.set_obstacle(grid[row][column].is_obstacle())
            new_grid_row.append(node)
        new_grid.append(new_grid_row)
    return new_grid


def save_immediate_result(astar_grid: List[List[AStarNode]]):
    result = []
    for row in range(len(astar_grid)):
        temp_row = []
        for column in range(len(astar_grid[row])):
            node = astar_grid[row][column]
            temp_row.append(PathFindingState(x=column,
                                             y=row,
                                             visited=node.visited,
                                             distance=node.get_distance(),
                                             previous=(node.previous.x, node.previous.y) if node.previous else None,
                                             debug_text=node.debug_text()))
        result.append(temp_row)
    return result


def a_star(grid: List[List[PathFindingNode]],
           origin: PathFindingNode,
           destination: PathFindingNode):
    a_star_grid = copy_grid(grid)
    a_star_origin = a_star_grid[origin.y][origin.x]
    a_star_destination = a_star_grid[destination.y][destination.x]

    # set the distance to be 0 for origin
    a_star_origin.set_g(0)
    a_star_origin.set_h(0)

    # initialize the priority queue
    unvisited_list = PriorityHeapQueue([], comparator)
    for y in range(len(a_star_grid)):
        for x in range(len(a_star_grid[y])):
            if check_valid_block(x, y, a_star_grid):
                unvisited_list.insert(a_star_grid[y][x])

    animation: List[List[List[PathFindingState]]] = []

    # if unvisited list is not empty and the destination node is not visited yet
    while not unvisited_list.is_empty() and not a_star_destination.get_visited():
        current_node = unvisited_list.pop()
        current_node.set_visited()
        for neighbor in neighbors:
            neighbor_x = current_node.x + neighbor['coordinate'][0]
            neighbor_y = current_node.y + neighbor['coordinate'][1]
            if check_valid_block(neighbor_x, neighbor_y, a_star_grid):
                update_node_distance(a_star_grid[neighbor_y][neighbor_x],
                                     current_node,
                                     a_star_destination,
                                     neighbor['distance'])
        animation.append(save_immediate_result(a_star_grid))

    path_found = destination.get_visited()
    return path_found, animation
