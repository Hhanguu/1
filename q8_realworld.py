"""
module8_realworld.py - Q8: Mang luoi phan phoi nuoc
Khong su dung bat ky thu vien nao
"""

from graph import Graph



def create_water_network():
    edges = [
        (0, 1, 15), (0, 2, 12), (0, 3, 10),
        (1, 4, 8), (1, 5, 7), (2, 5, 6), (2, 6, 9),
        (3, 6, 5), (3, 7, 8), (4, 8, 6), (4, 9, 4),
        (5, 9, 5), (5, 10, 7), (6, 10, 6), (6, 11, 8),
        (7, 11, 5), (7, 12, 6), (8, 13, 7), (9, 13, 4),
        (9, 14, 5), (10, 14, 6), (10, 15, 4), (11, 15, 7),
        (11, 16, 5), (12, 16, 6), (12, 17, 4), (13, 18, 6),
        (14, 18, 5), (15, 18, 7), (16, 19, 8), (17, 19, 6), (18, 19, 10),
    ]
    g = Graph(nodes=list(range(20)), edges=edges, is_directed=True, weighted=True)
    g._source = 0
    g._sink = 19
    return g


def get_cap(graph, u, v):
    for nb, w in graph.get_neighbors(u):
        if nb == v:
            return w
    return 0


def bfs_aug(graph, source, sink, flow):
    visited = {}
    parent = {}
    queue = [source]
    visited[source] = 1
    while len(queue) > 0:
        u = queue.pop(0)
        for v, w in graph.get_neighbors(u):
            r = w - flow.get((u, v), 0)
            if v not in visited and r > 0:
                visited[v] = 1
                parent[v] = u
                queue.append(v)
                if v == sink:
                    path = []
                    cur = sink
                    while cur != source:
                        path.append((parent[cur], cur))
                        cur = parent[cur]
                    path.reverse()
                    return path
    return None


def ford_fulkerson(graph, source, sink):
    flow = {}
    max_flow = 0
    step = 0
    while True:
        path = bfs_aug(graph, source, sink, flow)
        if path is None:
            break
        min_r = 999999999
        for u, v in path:
            r = get_cap(graph, u, v) - flow.get((u, v), 0)
            if r < min_r:
                min_r = r
        for u, v in path:
            flow[(u, v)] = flow.get((u, v), 0) + min_r
            flow[(v, u)] = flow.get((v, u), 0) - min_r
        max_flow += min_r
        step += 1
        path_str = " -> ".join(str(u) for u, v in path) + " -> " + str(sink)
        print("  Buoc " + str(step) + ": " + path_str + " (+" + str(min_r) + ")")
    return flow, max_flow


def run_module8():
    print("\n" + "=" * 60)
    print("  MODULE 8: BAI TOAN THUC TE - MANG LUOI NUOC")
    print("=" * 60)
    print("""
Mo ta bai toan:
  20 diem phan phoi nuoc thanh pho:
  - Diem 0: Nha may loc nuoc (NGUON)
  - Diem 1-18: Giao diem phan phoi
  - Diem 19: Khu dan cu (DICH)
  - Canh = ong dan voi dung luong toi da (m3/gio)
  - Ap dung: Ford-Fulkerson
""")

    graph = create_water_network()
    graph._source = 0
    graph._sink = 19

    print("Do thi: " + str(len(graph.nodes)) + " diem, " + str(len(graph.get_all_edges())) + " ong dan")

    print("\nDung luong cac ong dan:")
    for u, v, w in graph.get_all_edges():
        print("  " + str(u).rjust(2) + " -> " + str(v).rjust(2) + ": " + str(w) + " m3/gio")

    print("\n" + "-" * 40)
    print("  FORD-FULKERSON")
    print("-" * 40)

    flow, max_flow = ford_fulkerson(graph, 0, 19)

    print("\n" + "=" * 40)
    print("  LUONG NUOC TOI DA = " + str(max_flow) + " m3/gio")
    print("=" * 40)

    print("\nLuong tren moi ong dan:")
    for u, v, w in graph.get_all_edges():
        f = flow.get((u, v), 0)
        if f > 0:
            print("  " + str(u).rjust(2) + " -> " + str(v).rjust(2) + ": " + str(f) + "/" + str(w) + " m3/gio")

    cap_dict = {}
    for u, v, w in graph.get_all_edges():
        cap_dict[(u, v)] = w

    hl = [(u, v) for u, v, w in graph.get_all_edges() if flow_w.get((u, v), 0) > 0]
    graph.draw_graph(
        filename="graph_water.png",
        title="Mang luoi nuoc - Luong toi da",
        highlight_edges=hl,
    )
    print("  Da luu: graph_water.png")

    print("\n--- Hoan thanh Module 8 ---")


if __name__ == "__main__":
    run_module8()
