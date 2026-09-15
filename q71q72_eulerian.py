"""
module5_eulerian.py - Q7.1 & Q7.2: Fleury & Hierholzer
Khong su dung bat ky thu vien nao
"""

from graph import Graph
from examples import create_eulerian_graph



def find_start_node(graph):
    odd_nodes = []
    for node in graph.nodes:
        deg = graph.get_degree(node)
        if deg % 2 == 1:
            odd_nodes.append(node)
    if len(odd_nodes) == 0:
        return graph.nodes[0]
    elif len(odd_nodes) == 2:
        return odd_nodes[0]
    return None


def check_eulerian(graph):
    odd_nodes = []
    for node in graph.nodes:
        if graph.get_degree(node) % 2 == 1:
            odd_nodes.append(node)
    if len(odd_nodes) == 0:
        return "Euler Circuit"
    elif len(odd_nodes) == 2:
        return "Euler Path"
    return None


def is_bridge(graph, u, v):
    def count_components(g):
        visited = {}
        count = 0
        for node in g.nodes:
            if node not in visited:
                count += 1
                stack = [node]
                while len(stack) > 0:
                    n = stack.pop()
                    if n in visited:
                        continue
                    visited[n] = 1
                    for nb, w in g.get_neighbors(n):
                        if nb not in visited:
                            stack.append(nb)
        return count

    g_temp = graph.copy()
    g_temp.remove_edge(u, v)
    if not graph.is_directed:
        g_temp.remove_edge(v, u)
    return count_components(g_temp) > count_components(graph)


def fleury(graph, start=None):
    if start is None:
        start = find_start_node(graph)
    if start is None:
        return None
    g = graph.copy()
    path_edges = []
    current = start
    while True:
        neighbors = g.get_neighbors(current)
        if len(neighbors) == 0:
            break
        next_node = None
        for nb, w in neighbors:
            if len(neighbors) == 1:
                next_node = nb
                break
            if not is_bridge(g, current, nb):
                next_node = nb
                break
        if next_node is None:
            next_node = neighbors[0][0]
        path_edges.append((current, next_node))
        g.remove_edge(current, next_node)
        if not g.is_directed:
            g.remove_edge(next_node, current)
        current = next_node
    return path_edges


def hierholzer(graph, start=None):
    if start is None:
        start = find_start_node(graph)
    if start is None:
        return None
    g = graph.copy()
    stack = [start]
    circuit = []
    while len(stack) > 0:
        u = stack[-1]
        neighbors = g.get_neighbors(u)
        if len(neighbors) > 0:
            v, w = neighbors[0]
            stack.append(v)
            g.remove_edge(u, v)
            if not g.is_directed:
                g.remove_edge(v, u)
        else:
            circuit.append(stack.pop())
    circuit.reverse()
    return circuit


def run_module5():
    print("\n" + "=" * 60)
    print("  MODULE 7.1 & 7.2: DUONG/CU TRINH EULER")
    print("  Fleury & Hierholzer")
    print("=" * 60)

    print("\nChon do thi:")
    print("  1. Do thi Euler mau (10 dinh)")
    print("  2. Do thi 20 dinh")
    choice = input("Chon (1-2): ").strip()

    if choice == "1":
        graph = create_eulerian_graph()
    elif choice == "2":
        from examples import create_20_undirected
        graph = create_20_undirected()
    else:
        graph = create_eulerian_graph()

    print("\nDo thi: " + str(len(graph.nodes)) + " dinh, " + str(len(graph.get_all_edges())) + " canh")
    print("\nBac cua moi dinh:")
    for node in graph.nodes:
        deg = graph.get_degree(node)
        chan_le = "chan" if deg % 2 == 0 else "LE"
        print("  Dinh " + str(node) + ": bac " + str(deg) + " (" + chan_le + ")")

    euler_type = check_eulerian(graph)
    if euler_type:
        print("\n=> " + euler_type)
    else:
        print("\n=> DO THI KHONG CO DUONG/CU TRINH EULER")
        return

    # FLEURY
    print("\n" + "-" * 40)
    print("  FLEURY ALGORITHM")
    print("-" * 40)
    result_fleury = fleury(graph)
    if result_fleury:
        path_str = str(result_fleury[0][0])
        for u, v in result_fleury:
            path_str += " -> " + str(v)
        print("  " + path_str)
        print("  So canh: " + str(len(result_fleury)))

    # HIERHOLZER
    print("\n" + "-" * 40)
    print("  HIERHOLZER ALGORITHM")
    print("-" * 40)
    result_hier = hierholzer(graph)
    if result_hier:
        print("  " + " -> ".join(str(x) for x in result_hier))
        print("  So dinh: " + str(len(result_hier)))

    if result_hier:
        eh = []
        for i in range(len(result_hier) - 1):
            eh.append((result_hier[i], result_hier[i + 1]))

    graph.draw_graph(
        filename="graph_eulerian.png",
        title="Duong/Cu trinh Euler (Hierholzer)",
        highlight_edges=eh if result_hier else None,
    )
    print("  Da luu: graph_eulerian.png")

    print("\n--- Hoan thanh Module 5 ---")


if __name__ == "__main__":
    run_module5()
