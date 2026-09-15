"""
run_all.py - Chay tat ca thuat toan tren do thi mau 10 dinh A-J
Tao file docx voi bang ket qua chi tiet
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import Graph
from examples import create_sample_graph
from collections import deque
import heapq


# ============================================================
# GRAPH DATA (from image: 10 vertices, 21 edges)
# ============================================================
def create_graph_10():
    edges = [
        ("A", "B", 4), ("A", "C", 2), ("A", "D", 7),
        ("B", "C", 1), ("B", "E", 5),
        ("C", "D", 2), ("C", "E", 3), ("C", "F", 4),
        ("D", "C", 5), ("D", "G", 6),
        ("E", "F", 3), ("E", "H", 5),
        ("F", "G", 2), ("F", "I", 6), ("F", "J", 1),
        ("G", "I", 1), ("G", "J", 4),
        ("H", "I", 3), ("H", "J", 2),
        ("I", "J", 4),
    ]
    return Graph(
        nodes=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        edges=edges, is_directed=True, weighted=True
    )


# ============================================================
# BFS
# ============================================================
def bfs(graph, start):
    visited = {start: 1}
    queue = [start]
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        neighbors = sorted([nb for nb, w in graph.get_neighbors(node) if nb not in visited])
        for nb in neighbors:
            visited[nb] = 1
            queue.append(nb)
    return order


# ============================================================
# DFS
# ============================================================
def dfs(graph, start):
    visited = {}
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited[node] = 1
        order.append(node)
        neighbors = sorted([nb for nb, w in graph.get_neighbors(node) if nb not in visited], reverse=True)
        for nb in neighbors:
            stack.append(nb)
    return order


# ============================================================
# BIPARTITE CHECK
# ============================================================
def check_bipartite(graph):
    coloring = {}
    for node in graph.nodes:
        if node in coloring:
            continue
        queue = [node]
        coloring[node] = 0
        while queue:
            u = queue.pop(0)
            for v, w in graph.get_neighbors(u):
                if v not in coloring:
                    coloring[v] = 1 - coloring[u]
                    queue.append(v)
                elif coloring[v] == coloring[u]:
                    return False, coloring
    return True, coloring


# ============================================================
# GRAPH COLORING (Welsh-Powell)
# ============================================================
def graph_coloring(graph):
    nodes_by_degree = sorted(graph.nodes, key=lambda n: len(graph.get_neighbors(n)), reverse=True)
    color = {}
    for node in nodes_by_degree:
        used = {color[v] for v, w in graph.get_neighbors(node) if v in color}
        c = 0
        while c in used:
            c += 1
        color[node] = c
    return color, len(set(color.values()))


# ============================================================
# DIJKSTRA
# ============================================================
INF = 999999999

def dijkstra(graph, source):
    dist = {n: INF for n in graph.nodes}
    parent = {n: None for n in graph.nodes}
    dist[source] = 0
    visited = {}
    for _ in range(len(graph.nodes)):
        u = None
        min_d = INF
        for n in graph.nodes:
            if n not in visited and dist[n] < min_d:
                min_d = dist[n]
                u = n
        if u is None:
            break
        visited[u] = 1
        for v, w in graph.get_neighbors(u):
            if v not in visited and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    return dist, parent


def trace_path(parent, source, target):
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path if path and path[0] == source else None


# ============================================================
# BELLMAN-FORD
# ============================================================
def bellman_ford(graph, source):
    dist = {n: INF for n in graph.nodes}
    parent = {n: None for n in graph.nodes}
    dist[source] = 0
    edges = graph.get_all_edges()

    for i in range(len(graph.nodes) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] < INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break

    has_neg = False
    for u, v, w in edges:
        if dist[u] < INF and dist[u] + w < dist[v]:
            has_neg = True
            break
    return dist, parent, has_neg


# ============================================================
# UNION-FIND
# ============================================================
class UnionFind:
    def __init__(self, elements):
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


# ============================================================
# PRIM
# ============================================================
def prim(graph, start=None):
    if start is None:
        start = graph.nodes[0]
    in_tree = {start: 1}
    mst_edges = []
    total = 0
    for _ in range(len(graph.nodes) - 1):
        best_edge = None
        best_w = INF
        for node in in_tree:
            for nb, w in graph.get_neighbors(node):
                if nb not in in_tree and w < best_w:
                    best_w = w
                    best_edge = (node, nb, w)
        if best_edge is None:
            break
        u, v, w = best_edge
        mst_edges.append(best_edge)
        total += w
        in_tree[v] = 1
    return mst_edges, total


# ============================================================
# KRUSKAL
# ============================================================
def kruskal(graph):
    all_edges = graph.get_all_edges()
    sorted_edges = sorted(all_edges, key=lambda e: e[2])
    uf = UnionFind(graph.nodes)
    mst_edges = []
    total = 0
    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total += w
        if len(mst_edges) == len(graph.nodes) - 1:
            break
    return mst_edges, total


# ============================================================
# EULER CHECK + HIERHOLZER
# ============================================================
def check_eulerian(graph):
    odd_nodes = []
    for node in graph.nodes:
        if graph.get_degree(node) % 2 == 1:
            odd_nodes.append(node)
    if len(odd_nodes) == 0:
        return "Euler Circuit", odd_nodes
    elif len(odd_nodes) == 2:
        return "Euler Path", odd_nodes
    return None, odd_nodes


def hierholzer(graph, start=None):
    odd_nodes = []
    for node in graph.nodes:
        if graph.get_degree(node) % 2 == 1:
            odd_nodes.append(node)

    if len(odd_nodes) == 0:
        start = start or graph.nodes[0]
    elif len(odd_nodes) == 2:
        start = start if start in odd_nodes else odd_nodes[0]
    else:
        return None

    g = graph.copy()
    stack = [start]
    circuit = []
    while stack:
        u = stack[-1]
        neighbors = g.get_neighbors(u)
        if neighbors:
            v, w = neighbors[0]
            stack.append(v)
            g.remove_edge(u, v)
            if not g.is_directed:
                g.remove_edge(v, u)
        else:
            circuit.append(stack.pop())
    circuit.reverse()
    return circuit


# ============================================================
# FORD-FULKERSON
# ============================================================
def get_capacity(graph, u, v):
    for nb, w in graph.get_neighbors(u):
        if nb == v:
            return w
    return 0


def bfs_augmenting_path(graph, source, sink, flow):
    visited = {source: 1}
    parent = {source: None}
    queue = [source]
    while queue:
        u = queue.pop(0)
        for v, w in graph.get_neighbors(u):
            residual = w - flow.get((u, v), 0)
            if v not in visited and residual > 0:
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
    steps = []
    while True:
        path = bfs_augmenting_path(graph, source, sink, flow)
        if path is None:
            break
        min_r = INF
        for u, v in path:
            r = get_capacity(graph, u, v) - flow.get((u, v), 0)
            if r < min_r:
                min_r = r
        for u, v in path:
            flow[(u, v)] = flow.get((u, v), 0) + min_r
            flow[(v, u)] = flow.get((v, u), 0) - min_r
        max_flow += min_r
        path_str = " -> ".join(str(u) for u, v in path) + " -> " + str(sink)
        steps.append((path_str, min_r))
    return flow, max_flow, steps


# ============================================================
# MAIN - CHAY TAT CA VA IN BANG
# ============================================================
def main():
    g = create_graph_10()

    print("=" * 70)
    print("   BANG TONG HOP KET QUA - DO THI MAU 10 DINH (A-J)")
    print("   Co huong, co trong so, 21 canh")
    print("=" * 70)

    # === Q1 & Q2: BIEU DIEN ===
    print("\n" + "=" * 70)
    print("  CHUONG I-II: BIEU DIEN DO THI")
    print("=" * 70)
    g.display_representations()

    # === Q3: BFS & DFS ===
    print("\n" + "=" * 70)
    print("  CHUONG III: DUYET BFS & DFS")
    print("=" * 70)
    for start in ["A", "B", "C"]:
        bfs_result = bfs(g, start)
        dfs_result = dfs(g, start)
        print(f"\n  Tu dinh '{start}':")
        print(f"    BFS: {' -> '.join(bfs_result)}")
        print(f"    DFS: {' -> '.join(dfs_result)}")

    # === Q4: BIPARTITE + COLORING ===
    print("\n" + "=" * 70)
    print("  CHUONG IV: KIEM TRA HAI PHIA & TO MAU")
    print("=" * 70)
    is_bip, coloring_bip = check_bipartite(g)
    print(f"\n  Do thi {'CO' if is_bip else 'KHONG'} la do thi hai phia.")
    if is_bip:
        set_a = sorted([n for n, c in coloring_bip.items() if c == 0])
        set_b = sorted([n for n, c in coloring_bip.items() if c == 1])
        print(f"    Phia A: {set_a}")
        print(f"    Phia B: {set_b}")

    color, num_colors = graph_coloring(g)
    print(f"\n  To mau (Welsh-Powell): {num_colors} mau can dung")
    for node in sorted(color.keys()):
        print(f"    {node}: mau {color[node]}")

    # === Q5: DIJKSTRA & BELLMAN-FORD ===
    print("\n" + "=" * 70)
    print("  CHUONG V: DUONG DI NGAN NHAT")
    print("=" * 70)
    source = "A"

    print(f"\n  --- Dijkstra (tu '{source}') ---")
    dist_d, parent_d = dijkstra(g, source)
    print(f"  {'Dinh':<6}{'Khoang cach':<14}{'Duong di'}")
    print(f"  {'-'*50}")
    for node in g.nodes:
        d = dist_d[node]
        d_str = str(d) if d < INF else "INF"
        p = trace_path(parent_d, source, node)
        p_str = " -> ".join(str(x) for x in p) if p else "Khong co"
        print(f"  {node:<6}{d_str:<14}{p_str}")

    print(f"\n  --- Bellman-Ford (tu '{source}') ---")
    dist_b, parent_b, has_neg = bellman_ford(g, source)
    if has_neg:
        print("  *** PHAT HIEN CHU TRINH AM! ***")
    else:
        print(f"  {'Dinh':<6}{'Khoang cach':<14}{'Duong di'}")
        print(f"  {'-'*50}")
        for node in g.nodes:
            d = dist_b[node]
            d_str = str(d) if d < INF else "INF"
            p = trace_path(parent_b, source, node)
            p_str = " -> ".join(str(x) for x in p) if p else "Khong co"
            print(f"  {node:<6}{d_str:<14}{p_str}")

    # === Q7.1 & Q7.2: EULER ===
    print("\n" + "=" * 70)
    print("  CHUONG VII.1-7.2: CHU TRINH / DUONG DI EULER")
    print("=" * 70)
    print("\n  Bac cua moi dinh:")
    for node in g.nodes:
        deg = g.get_degree(node)
        chan_le = "chan" if deg % 2 == 0 else "LE"
        print(f"    {node}: bac {deg} ({chan_le})")

    euler_type, odd_nodes = check_eulerian(g)
    if euler_type:
        print(f"\n  => {euler_type}")
        h_path = hierholzer(g)
        if h_path:
            print(f"  Hierholzer: {' -> '.join(str(x) for x in h_path)}")
    else:
        print(f"\n  => KHONG co duong/chu trinh Euler ({len(odd_nodes)} dinh bac le)")

    # === Q7.3 & Q7.4: MST (PRIM & KRUSKAL) ===
    print("\n" + "=" * 70)
    print("  CHUONG VII.3-7.4: CAY KHUNG NHO NHAT (MST)")
    print("=" * 70)
    print("  (Ap dung cho do thi vo huong - bo huong cac canh)")

    g_undirected = Graph(
        nodes=g.nodes,
        edges=[(u, v, w) for u, v, w in g.get_all_edges()],
        is_directed=False, weighted=True
    )

    print("\n  --- Prim ---")
    mst_p, w_p = prim(g_undirected)
    print(f"  {'Tu':<6}{'Den':<6}{'Trong so':<10}")
    print(f"  {'-'*22}")
    for u, v, w in mst_p:
        print(f"  {u:<6}{v:<6}{w:<10}")
    print(f"  Tong: {w_p}")

    print("\n  --- Kruskal ---")
    mst_k, w_k = kruskal(g_undirected)
    print(f"  {'Tu':<6}{'Den':<6}{'Trong so':<10}")
    print(f"  {'-'*22}")
    for u, v, w in mst_k:
        print(f"  {u:<6}{v:<6}{w:<10}")
    print(f"  Tong: {w_k}")
    print(f"  Khop: {'Co' if w_p == w_k else 'Khong'}")

    # === Q7.5: FORD-FULKERSON ===
    print("\n" + "=" * 70)
    print("  CHUONG VII.5: LUONG TOI DA (FORD-FULKERSON)")
    print("=" * 70)
    print("  (Ap dung cho do thi co huong - goc A, dich J)")

    flow, max_flow, steps = ford_fulkerson(g, "A", "J")
    for i, (path_str, delta) in enumerate(steps, 1):
        print(f"  Buoc {i}: {path_str} (+{delta})")
    print(f"\n  LUONG TOI DA: {max_flow}")

    print("\n  Luong tren canh:")
    for u, v, w in g.get_all_edges():
        f = flow.get((u, v), 0)
        if f > 0:
            print(f"    {u} -> {v}: {f}/{w}")

    # === VE DO THI ===
    print("\n" + "=" * 70)
    print("  VE DO THI")
    print("=" * 70)
    g.draw_graph(filename="dothi_10dinh.png", title="Do thi mau 10 dinh - 21 canh")
    print("  Da luu: dothi_10dinh.png")

    print("\n" + "=" * 70)
    print("   HOAN THANH!")
    print("=" * 70)


if __name__ == "__main__":
    main()
