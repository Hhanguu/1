"""
module4_shortest.py - Q5: Dijkstra & Bellman-Ford
Khong su dung bat ky thu vien nao
"""

from graph import Graph
from examples import create_sample_graph, create_small_directed, create_20_undirected, create_20_directed

INF = 999999999


def dijkstra(graph, source):
    dist = {}
    parent = {}
    visited = {}
    for node in graph.nodes:
        dist[node] = INF
        parent[node] = None
    dist[source] = 0

    for _ in range(len(graph.nodes)):
        u = None
        min_d = INF
        for node in graph.nodes:
            if node not in visited and dist[node] < min_d:
                min_d = dist[node]
                u = node
        if u is None:
            break
        visited[u] = 1
        for v, w in graph.get_neighbors(u):
            if v not in visited:
                new_d = dist[u] + w
                if new_d < dist[v]:
                    dist[v] = new_d
                    parent[v] = u
    return dist, parent


def bellman_ford(graph, source):
    dist = {}
    parent = {}
    for node in graph.nodes:
        dist[node] = INF
        parent[node] = None
    dist[source] = 0

    for i in range(len(graph.nodes) - 1):
        updated = False
        for u, v, w in graph.get_all_edges():
            if dist[u] < INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            print("  Lap thu " + str(i + 1) + ": Khong cap nhat -> dung som")
            break
        else:
            print("  Lap thu " + str(i + 1) + ": Co cap nhat")

    has_neg = False
    for u, v, w in graph.get_all_edges():
        if dist[u] < INF and dist[u] + w < dist[v]:
            has_neg = True
            break
    return dist, parent, has_neg


def trace_path(parent, source, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    if len(path) == 0 or path[0] != source:
        return None
    return path


def run_module4():
    print("\n" + "=" * 60)
    print("  MODULE 5: DUONG DI NGAN NHAT")
    print("  Dijkstra & Bellman-Ford (Cau 5)")
    print("=" * 60)

    print("\nChon do thi:")
    print("  1. Do thi mau A-J (10 dinh)")
    print("  2. Do thi nho CO HUONG (6 dinh)")
    print("  3. Do thi 20 dinh VO HUONG")
    print("  4. Do thi 20 dinh CO HUONG (co canh am)")
    choice = input("Chon (1-4): ").strip()

    if choice == "1":
        graph = create_sample_graph()
    elif choice == "2":
        graph = create_small_directed()
    elif choice == "3":
        graph = create_20_undirected()
    elif choice == "4":
        graph = create_20_directed()
    else:
        graph = create_sample_graph()

    print("\nDo thi: " + str(len(graph.nodes)) + " dinh, " + str(len(graph.get_all_edges())) + " canh")

    while True:
        try:
            source = input("\nNhap dinh nguon " + str(graph.nodes) + ": ").strip()
            try:
                source = int(source)
            except Exception:
                pass
            if source in graph.nodes:
                break
            print("Dinh khong ton tai!")
        except Exception:
            print("Nhap sai!")

    while True:
        try:
            target = input("Nhap dinh dich " + str(graph.nodes) + ": ").strip()
            try:
                target = int(target)
            except Exception:
                pass
            if target in graph.nodes:
                break
            print("Dinh khong ton tai!")
        except Exception:
            print("Nhap sai!")

    # DIJKSTRA
    print("\n" + "-" * 40)
    print("  DIJKSTRA")
    print("-" * 40)

    dist_d, parent_d = dijkstra(graph, source)
    print("\nBang khoang cach tu dinh " + str(source) + ":")
    print("  Dinh  | Khoang cach | Duong di")
    print("  " + "-" * 40)
    for node in graph.nodes:
        d = dist_d[node]
        d_str = str(d) if d < INF else "INF"
        p = trace_path(parent_d, source, node)
        p_str = " -> ".join(str(x) for x in p) if p else "Khong co"
        print("  " + str(node).rjust(5) + " | " + d_str.rjust(11) + " | " + p_str)

    path_d = trace_path(parent_d, source, target)
    if path_d:
        print("\nDuong di ngan nhat " + str(source) + " -> " + str(target) + ":")
        print("  " + " -> ".join(str(x) for x in path_d))
        print("  Chi phi: " + str(dist_d[target]))

    if path_d:
        eh = []
        for i in range(len(path_d) - 1):
            eh.append((path_d[i], path_d[i + 1]))
        nc = {}
        for n in path_d:
            nc[n] = "orange"

    # BELLMAN-FORD
    print("\n" + "-" * 40)
    print("  BELLMAN-FORD")
    print("-" * 40)

    dist_b, parent_b, has_neg = bellman_ford(graph, source)
    if has_neg:
        print("\n  *** PHAT HIEN CHU TRINH AM! ***")
    else:
        path_b = trace_path(parent_b, source, target)
        if path_b:
            print("\nDuong di ngan nhat " + str(source) + " -> " + str(target) + ":")
            print("  " + " -> ".join(str(x) for x in path_b))
            print("  Chi phi: " + str(dist_b[target]))

    hl_edges = []
    nc = {}
    if path_d:
        for i in range(len(path_d) - 1):
            hl_edges.append((path_d[i], path_d[i + 1]))
        for n in path_d:
            nc[n] = "orange"

    graph.draw_graph(
        filename="graph_shortest.png",
        title="Duong di ngan nhat (Dijkstra)",
        node_colors=nc if nc else None,
        highlight_edges=hl_edges,
    )
    print("  Da luu: graph_shortest.png")

    print("\n--- Hoan thanh Module 4 ---")


if __name__ == "__main__":
    run_module4()
