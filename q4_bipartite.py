"""
module3_bipartite.py - Q4: Kiem tra do thi hai phia (Bipartite)
Khong su dung bat ky thu vien nao
"""

from graph import Graph
from examples import create_sample_graph, create_20_undirected



def check_bipartite(graph):
    coloring = {}
    unvisited = {}
    for node in graph.nodes:
        unvisited[node] = 1

    while len(unvisited) > 0:
        start = None
        for node in sorted(unvisited.keys()):
            start = node
            break
        if start is None:
            break

        queue = [start]
        coloring[start] = 0
        del unvisited[start]

        while len(queue) > 0:
            node = queue.pop(0)
            current_color = coloring[node]
            for nb, w in graph.get_neighbors(node):
                if nb in coloring:
                    if coloring[nb] == current_color:
                        return False, None
                else:
                    coloring[nb] = 1 - current_color
                    if nb in unvisited:
                        del unvisited[nb]
                    queue.append(nb)

    return True, coloring


def run_module3():
    print("\n" + "=" * 60)
    print("  MODULE 4: KIEM TRA DO THI HAI PHIA (BIPARTITE)")
    print("  (Cau 4)")
    print("=" * 60)

    print("\nChon do thi:")
    print("  1. Do thi mau A-J (10 dinh)")
    print("  2. Do thi 20 dinh VO HUONG")
    print("  3. Do thi test Bipartite (5 dinh)")
    print("  4. Do thi test KHONG Bipartite (4 dinh)")
    print("  5. Nhap tu ban phim")
    choice = input("Chon (1-5): ").strip()

    if choice == "1":
        graph = create_sample_graph()
    elif choice == "2":
        graph = create_20_undirected()
    elif choice == "3":
        edges = [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1), (2, 4, 1)]
        graph = Graph(nodes=[0, 1, 2, 3, 4], edges=edges, is_directed=False, weighted=False)
    elif choice == "4":
        edges = [(0, 1, 1), (1, 2, 1), (2, 0, 1), (0, 3, 1)]
        graph = Graph(nodes=[0, 1, 2, 3], edges=edges, is_directed=False, weighted=False)
    else:
        from q1q2_repr import input_graph_manual
        graph = input_graph_manual()

    print("\nDo thi: " + str(len(graph.nodes)) + " dinh, " + str(len(graph.get_all_edges())) + " canh")
    is_bip, coloring = check_bipartite(graph)
    nc = None

    if is_bip:
        print("\n=> DO THI LA DO THI HAI PHIA (BIPARTITE)")
        set_a = []
        set_b = []
        for node in sorted(coloring.keys()):
            if coloring[node] == 0:
                set_a.append(node)
            else:
                set_b.append(node)
        print("  Tap A: " + str(set_a))
        print("  Tap B: " + str(set_b))

        nc = {}
        for node in coloring:
            if coloring[node] == 0:
                nc[node] = (0.2, 0.6, 1.0)
            else:
                nc[node] = (1.0, 0.3, 0.3)
    else:
        print("\n=> DO THI KHONG PHAI LA DO THI HAI PHIA")

    graph.draw_graph(
        filename="graph_bipartite.png",
        title="Bipartite Check",
        node_colors=nc if is_bip else None,
    )
    print("  Da luu: graph_bipartite.png")

    print("\n--- Hoan thanh Module 3 ---")


if __name__ == "__main__":
    run_module3()
