import sys
from typing import List
from Vertex import Vertex
from Graph import Graph


def graph_init(g: Graph):
    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b', 7)
    g.add_edge('a', 'c', 9)
    g.add_edge('a', 'f', 14)
    g.add_edge('b', 'c', 10)
    g.add_edge('b', 'd', 15)
    g.add_edge('c', 'd', 11)
    g.add_edge('c', 'f', 2)
    g.add_edge('d', 'e', 6)
    g.add_edge('e', 'f', 9)
    return g


# @params unvisited list
# @return the DijkstraDijkstraDijkstraNode with the shortest distance to the origin
def find_nearest_node(unvisited_list: List[Vertex]) -> Vertex:
    shortest_distance = sys.maxsize
    nearest_node = None
    for vertex in unvisited_list:
        if vertex.get_distance() <= shortest_distance:
            shortest_distance = vertex.get_distance()
            nearest_node = vertex
    return nearest_node


# @params visited_node: the node to be removed
# @params unvisited_list: the reference of the unvisited list
# @return void
def remove_visited_node(visited_node: Vertex, unvisited_list: List[Vertex]):
    for vertex in unvisited_list:
        if vertex.get_id() == visited_node.get_id():
            unvisited_list.remove(vertex)


def dijkstra(graph: Graph, origin: Vertex):
    # set the distance of the origin to 0
    origin.set_distance(0)

    # create an unvisited vertex list
    # push all the node other than the origin to the list
    unvisited_list = []
    for vertex in graph:
        unvisited_list.append(vertex)

    while len(unvisited_list) > 0:
        # Find the nearest vertex first (vertex with the smallest distance)
        current_vertex = find_nearest_node(unvisited_list)

        # Set the current vertex to be "visited"
        current_vertex.set_visited()
        # Remove the current vertex from the unvisited list
        remove_visited_node(current_vertex, unvisited_list)

        print(f'Neighbor of {current_vertex.get_id()}:')
        # Find all the neighbor vertex of the nearest node
        for neighbor in current_vertex.adjacent:
            # Skip the visited vertex
            if neighbor.get_visited():
                continue
            print(neighbor.get_id())
            new_distance = current_vertex.get_distance() + current_vertex.get_weight(neighbor)
            print(f'New Distance = {str(new_distance)}')
            if neighbor.get_distance() > new_distance:
                print(f"Updated for the vertex {neighbor.get_id()} "
                      f"(New Distance {new_distance} > Original Distance {neighbor.get_distance()})")
                neighbor.set_previous(current_vertex)
                neighbor.set_distance(new_distance)
            else:
                print(f"Not Updated for the vertex {neighbor.get_id()} "
                      f"(New Distance {new_distance} < Original Distance {neighbor.get_distance()})")

    return graph


def debug_graph(g):
    for v in g:
        print(f'DijkstraDijkstraNode {v.get_id()}')
        print(f'Distance: {v.get_distance()}')
        path = v.get_id()
        current = v
        while current.get_previous():
            path = path + '->' + current.get_previous().get_id()
            current = current.get_previous()
        print(f'Shortest Path: {path}')


def main():
    print("This is the implementation of the dijkstra algorithm")
    g = Graph()
    graph_init(g)
    dijkstra(g, g.get_vertex('e'))
    debug_graph(g)


if __name__ == "__main__":
    main()
