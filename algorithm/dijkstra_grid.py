import copy
from typing import List, Union
from algorithm.DijkstraNode import DijkstraNode
from algorithm.PriorityHeapQueue import PriorityHeapQueue

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


def dijkstra(grid: List[List[DijkstraNode]], origin: DijkstraNode, destination: DijkstraNode = None):
    # set the distance of the origin to 0
    origin.set_distance(0)

    # create an unvisited vertex list
    # push all the node other than the origin to the list
    unvisited_list = PriorityHeapQueue([], comparator)
    for nodeList in grid:
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
    search_result: List[List[List[DijkstraNode]]] = []

    while not unvisited_list.is_empty() and not destination.get_visited():
        # Find the nearest node first (node with the smallest distance)
        current_node = unvisited_list.pop()

        # Set the current node to be "visited"
        current_node.set_visited()
        for neighbor in neighbors:
            neighbor_x = current_node.x + neighbor['coordinate'][0]
            neighbor_y = current_node.y + neighbor['coordinate'][1]

            if check_valid_block(neighbor_x, neighbor_y, grid):
                update_node_distance(grid[neighbor_y][neighbor_x],
                                     current_node,
                                     neighbor['distance'])
        search_result.append(copy.deepcopy(grid))

    # debug_unvisited_list(unvisited_list)
    path_found = destination.get_visited()
    return path_found, search_result


if __name__ == '__main__':
    # initialize the grid
    test_grid: List[List[DijkstraNode]] = []
    init_grid(test_grid, ROW, COLUMN)
    print("-------after path finding--------")

    origin = test_grid[0][0]
    destination = test_grid[0][9]
    test_grid[0][1].set_obstacle()
    test_grid[0][2].set_obstacle()
    test_grid[0][3].set_obstacle()
    test_grid[0][4].set_obstacle()
    test_grid[0][5].set_obstacle()
    test_grid[0][6].set_obstacle()
    test_grid[1][1].set_obstacle()
    test_grid[1][2].set_obstacle()
    test_grid[1][3].set_obstacle()
    test_grid[2][2].set_obstacle()
    path_found, search_result = dijkstra(test_grid, origin, destination)
    print(path_found)
    # debug_grid(test_grid)
    debug_shortest_path(test_grid, origin, destination)
