from typing import List, Union
from algorithm.DijkstraNode import DijkstraNode
from algorithm.PriorityQueue import PriorityQueue

ROW = 10
COLUMN = 10
VERTICAL_DISTANCE = 1
HORIZONTAL_DISTANCE = 1
DIAGONAL_DISTANCE = 1.4  # sqrt(2)


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
            print(f"Updated for the vertex {str(compared_node)}"
                  f"(New Distance {new_distance} > Original Distance {compared_node.get_distance()})")
        else:
            print(f"Updated for the vertex {str(compared_node)}"
                  f"(New Distance {new_distance} < Original Distance {compared_node.get_distance()})")


def check_destination(destination: DijkstraNode = None) -> bool:
    if destination is None:
        return True
    if destination.get_visited():
        return False
    return True


def check_out_of_range(x: int, y: int, grid: List[List[DijkstraNode]]) -> bool:
    # Check the node is inside the grid and not an obstacle
    if 0 <= y < len(grid) and 0 <= x < len(grid[y]) and not grid[y][x].is_obstacle():
        return True
    return False


def dijkstra(grid: List[List[DijkstraNode]], origin: DijkstraNode, destination: DijkstraNode = None):
    # set the distance of the origin to 0
    origin.set_distance(0)

    # create an unvisited vertex list
    # push all the node other than the origin to the list
    unvisited_list = PriorityQueue()
    for nodeList in grid:
        for node in nodeList:
            if not node.is_obstacle():
                unvisited_list.insert(node)

    while not unvisited_list.is_empty() and check_destination(destination):
        print(check_destination(destination))
        # Find the nearest node first (node with the smallest distance)
        x, y = unvisited_list.pop()
        current_node = grid[y][x]

        # Set the current node to be "visited"
        current_node.set_visited()

        print(f'Current DijkstraNode {str(current_node)}:')

        # Find all the neighbor nodes (vertical, horizontal, diagonal)
        # top
        if check_out_of_range(current_node.x, current_node.y - 1, grid):
            update_node_distance(grid[current_node.y - 1][current_node.x], current_node, VERTICAL_DISTANCE)

        # top-left
        if check_out_of_range(current_node.x - 1, current_node.y - 1, grid):
            update_node_distance(grid[current_node.y - 1][current_node.x - 1], current_node, DIAGONAL_DISTANCE)

        # top-right
        if check_out_of_range(current_node.x + 1, current_node.y - 1, grid):
            update_node_distance(grid[current_node.y - 1][current_node.x + 1], current_node, DIAGONAL_DISTANCE)

        # left
        if check_out_of_range(current_node.x - 1, current_node.y, grid):
            update_node_distance(grid[current_node.y][current_node.x - 1], current_node, HORIZONTAL_DISTANCE)

        # right
        if check_out_of_range(current_node.x + 1, current_node.y, grid):
            update_node_distance(grid[current_node.y][current_node.x + 1], current_node, HORIZONTAL_DISTANCE)

        # bottom-left
        if check_out_of_range(current_node.x - 1, current_node.y + 1, grid):
            update_node_distance(grid[current_node.y + 1][current_node.x - 1], current_node, DIAGONAL_DISTANCE)

        # bottom-right
        if check_out_of_range(current_node.x + 1, current_node.y + 1, grid):
            update_node_distance(grid[current_node.y + 1][current_node.x + 1], current_node, DIAGONAL_DISTANCE)

        # bottom
        if check_out_of_range(current_node.x, current_node.y + 1, grid):
            update_node_distance(grid[current_node.y + 1][current_node.x], current_node, VERTICAL_DISTANCE)
    return grid


if __name__ == '__main__':
    # initialize the grid
    test_grid: List[List[DijkstraNode]] = []
    init_grid(test_grid, ROW, COLUMN)
    debug_grid(test_grid)
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
    dijkstra(test_grid, origin, destination)
    debug_grid(test_grid)
    debug_shortest_path(test_grid, origin, destination)
