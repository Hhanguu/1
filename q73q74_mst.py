"""
module6_mst.py - Q7.3 & Q7.4: Prim & Kruskal
Khong su dung bat ky thu vien nao
"""

from graph import Graph
from examples import create_sample_graph, create_20_undirected



class UnionFind:
    def __init__(self, elements):
        self.parent = {}
        self.rank = {}
        for elem in elements:
            self.parent[elem] = elem
            self.rank[elem] = 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def prim(graph, start=None):
    if start is None:
        start = graph.nodes[0]
    in_tree = {}
    mst_edges = []
    total = 0
    in_tree[start] = 1

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


INF = 999999999


def kruskal(graph):
    all_edges = graph.get_all_edges()
    sorted_edges = []
    for e in all_edges:
        sorted_edges.append(e)
    for i in range(len(sorted_edges)):
        for j in range(i + 1, len(sorted_edges)):
            if sorted_edges[j][2] < sorted_edges[i][2]:
                sorted_edges[i], sorted_edges[j] = sorted_edges[j], sorted_edges[i]

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


def run_module6():
    print("\n" + "=" * 60)
    print("  MODULE 7.3 & 7.4: CAY KHUNG NHO NHAT (MST)")
    print("  Prim & Kruskal")
    print("=" * 60)

    print("\nChon do thi:")
    print("  1. Do thi mau A-J (10 dinh)")
    print("  2. Do thi 20 dinh VO HUONG")
    choice = input("Chon (1-2): ").strip()

    if choice == "1":
        graph = create_sample_graph()
    elif choice == "2":
        graph = create_20_undirected()
    else:
        graph = create_sample_graph()

    print("\nDo thi: " + str(len(graph.nodes)) + " dinh, " + str(len(graph.get_all_edges())) + " canh")

    # PRIM
    print("\n" + "-" * 40)
    print("  PRIM ALGORITHM")
    print("-" * 40)
    mst_p, w_p = prim(graph)
    print("  Tu    | Den   | Trong so")
    print("  " + "-" * 25)
    for u, v, w in mst_p:
        print("  " + str(u).rjust(5) + " | " + str(v).rjust(5) + " | " + str(w).rjust(8))
    print("  Tong trong so MST: " + str(w_p))

    eh = [(u, v) for u, v, w in mst_p]

    # KRUSKAL
    print("\n" + "-" * 40)
    print("  KRUSKAL ALGORITHM")
    print("-" * 40)
    mst_k, w_k = kruskal(graph)
    print("  Tu    | Den   | Trong so")
    print("  " + "-" * 25)
    for u, v, w in mst_k:
        print("  " + str(u).rjust(5) + " | " + str(v).rjust(5) + " | " + str(w).rjust(8))
    print("  Tong trong so MST: " + str(w_k))

    eh2 = [(u, v) for u, v, w in mst_k]

    graph.draw_graph(
        filename="graph_mst.png",
        title="Cay khung nho nhat (Kruskal)",
        highlight_edges=eh2,
    )
    print("  Da luu: graph_mst.png")

    print("\n--- Hoan thanh Module 6 ---")


if __name__ == "__main__":
    run_module6()
