import math
from typing import List, Union

from Node import Node
from AStarNode import AStarNode
from PriorityQueue import PriorityQueue

ROW = 10
COLUMN = 10
VERTICAL_DISTANCE = 1
HORIZONTAL_DISTANCE = 1
DIAGONAL_DISTANCE = 1.4  # sqrt(2)


def init_grid(grid: List[List[AStarNode]], row: int, column: int):
    for y in range(row):
        grid.append([])
        for x in range(column):
            grid[y].append(AStarNode(x, y))


def check_out_of_range(x: int, y: int, grid: List[List[AStarNode]]) -> bool:
    # Check the node is inside the grid and not an obstacle
    if 0 <= y < len(grid) and 0 <= x < len(grid[y]) and not grid[y][x].is_obstacle():
        return True
    return False


def update_node_distance(compared_node: AStarNode, current_node: AStarNode, destination: AStarNode,
                         weight: Union[int, float]):
    if not compared_node.get_visited():
        new_g = current_node.get_distance() + weight
        new_h = euclidean_distance(current_node, destination)
        new_distance = new_g + new_h
        if compared_node.get_distance() > new_distance:
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


def a_star(grid: List[List[AStarNode]], origin: AStarNode, destination: AStarNode):
    origin.set_g(0)
    origin.set_h(0)

    # initialize the priority queue
    unvisited_list = PriorityQueue()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            unvisited_list.insert(grid[y][x])

    # if unvisited list is not empty and the destination node is not visited yet
    while not unvisited_list.is_empty() or destination.get_visited():
        # the first current node should be the origin
        x, y = unvisited_list.pop()
        current_node = grid[y][x]
        print(f'Current AStarNode {str(current_node)}:')

        # Find all the neighbor nodes (vertical, horizontal, diagonal)
        # top
        if check_out_of_range(current_node.x, current_node.y - 1, grid):
            update_node_distance(grid[current_node.y - 1][current_node.x], current_node, destination, VERTICAL_DISTANCE)

        # top-left
        if check_out_of_range(current_node.x - 1, current_node.y - 1, grid):
            update_node_distance(grid[current_node.y - 1][current_node.x - 1], current_node, destination,
                                 DIAGONAL_DISTANCE)

        # top-right
        if check_out_of_range(current_node.x + 1, current_node.y - 1, grid):
            update_node_distance(grid[current_node.y - 1][current_node.x + 1], current_node, destination,
                                 DIAGONAL_DISTANCE)

        # left
        if check_out_of_range(current_node.x - 1, current_node.y, grid):
            update_node_distance(grid[current_node.y][current_node.x - 1], current_node, destination,
                                 HORIZONTAL_DISTANCE)

        # right
        if check_out_of_range(current_node.x + 1, current_node.y, grid):
            update_node_distance(grid[current_node.y][current_node.x + 1], current_node, destination,
                                 HORIZONTAL_DISTANCE)

        # bottom-left
        if check_out_of_range(current_node.x - 1, current_node.y + 1, grid):
            update_node_distance(grid[current_node.y + 1][current_node.x - 1], current_node, destination,
                                 DIAGONAL_DISTANCE)

        # bottom-right
        if check_out_of_range(current_node.x + 1, current_node.y + 1, grid):
            update_node_distance(grid[current_node.y + 1][current_node.x + 1], current_node, destination,
                                 DIAGONAL_DISTANCE)

        # bottom
        if check_out_of_range(current_node.x, current_node.y + 1, grid):
            update_node_distance(grid[current_node.y + 1][current_node.x], current_node, destination, VERTICAL_DISTANCE)
    return grid


def debug_shortest_path(grid: List[List[AStarNode]], origin: AStarNode, destination: AStarNode) -> float:
    # find the path first
    path: List[AStarNode] = []
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
            print(grid[y][x].distance_debug(), end='')
        print('')
    return destination.get_distance()


if __name__ == '__main__':
    test_grid: List[List[AStarNode]] = []
    init_grid(test_grid, ROW, COLUMN)
    test_origin = test_grid[0][0]
    test_destination = test_grid[5][0]
    test_grid[2][2].set_obstacle()
    test_grid[1][0].set_obstacle()
    test_grid[1][1].set_obstacle()
    test_grid[3][3].set_obstacle()
    a_star(test_grid, test_origin, test_destination)
    debug_shortest_path(test_grid, test_origin, test_destination)


