from typing import List, Union, Tuple
from algorithm.DijkstraNode import DijkstraNode
from algorithm.Node import Node
from algorithm.PathFindingState import PathFindingState
from algorithm.PriorityHeapQueue import PriorityHeapQueue
from ui.PathFindingNode import PathFindingNode

VERTICAL_DISTANCE = 1
HORIZONTAL_DISTANCE = 1
DIAGONAL_DISTANCE = 1.4  # sqrt(2)
DIJKSTRA = "Dijkstra"
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
            node = DijkstraNode(grid[row][column].x, grid[row][column].y)
            node.set_obstacle(grid[row][column].is_obstacle())
            new_grid_row.append(node)
        new_grid.append(new_grid_row)
    return new_grid


def save_immediate_result(dijkstra_grid: List[List[DijkstraNode]]):
    result = []
    for row in range(len(dijkstra_grid)):
        temp_row = []
        for column in range(len(dijkstra_grid[row])):
            node = dijkstra_grid[row][column]
            temp_row.append(PathFindingState(x=column,
                                             y=row,
                                             visited=node.visited,
                                             distance=node.get_distance(),
                                             previous=(node.previous.x, node.previous.y) if node.previous else None,
                                             debug_text=node.debug_text()))
        result.append(temp_row)
    return result


def dijkstra(
        grid: List[List[PathFindingNode]],
        origin: PathFindingNode, destination: PathFindingNode) \
        -> Tuple[bool, List[List[List[PathFindingState]]]]:
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

    animation: List[List[List[PathFindingState]]] = []

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

        animation.append(save_immediate_result(dijkstra_grid))

    path_found = dijkstra_grid_destination.get_visited()
    return path_found, animation
