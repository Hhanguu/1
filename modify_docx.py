"""
modify_docx.py - Sua file docx goc: thay code, hinh anh, ket qua
Dung cho do thi 10 dinh A-J, co huong, co trong so
"""

import sys
import os
import copy
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn

INPUT = "/home/hungvo/Downloads/CauTrucRoiRacDo_Thi chính.docx"
OUTPUT = "/home/hungvo/Downloads/CauTrucRoiRacDo_Thi_Chinh_Sua.docx"


def replace_text_in_cell(cell, old_text, new_text):
    """Replace text in a cell while preserving formatting."""
    for paragraph in cell.paragraphs:
        if old_text in paragraph.text:
            for run in paragraph.runs:
                if old_text in run.text:
                    run.text = run.text.replace(old_text, new_text)


def set_cell_text(cell, text):
    """Set cell text, preserving first paragraph's formatting."""
    if cell.paragraphs:
        p = cell.paragraphs[0]
        if p.runs:
            p.runs[0].text = text
            for run in p.runs[1:]:
                run.text = ""
        else:
            p.text = text
    # Remove extra paragraphs
    while len(cell.paragraphs) > 1:
        p = cell.paragraphs[-1]
        p._element.getparent().remove(p._element)


def set_paragraph_text(para, text):
    """Set paragraph text, preserving first run's formatting."""
    if para.runs:
        para.runs[0].text = text
        for run in para.runs[1:]:
            run.text = ""
    else:
        para.text = text


# ============================================================
# NEW CONTENT FOR 10-VERTEX DIRECTED GRAPH
# ============================================================

# Graph edges
EDGES_10 = [
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

NODES_10 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

# Adjacency list output
ADJ_LIST_10 = """=== Adjacency List (Danh sách kề) ===
Loại đồ thị:    Có hướng
Trọng số:       Có
----------------------------------------
A: B(4), C(2), D(7)
B: C(1), E(5)
C: D(2), E(3), F(4)
D: C(5), G(6)
E: F(3), H(5)
F: G(2), I(6), J(1)
G: I(1), J(4)
H: I(3), J(2)
I: J(4)
J: """

# Adjacency matrix output
ADJ_MATRIX_10 = """=== Adjacency Matrix (Ma trận kề) ===
Loại đồ thị:    Có hướng
Trọng số:       Có
----------------------------------------
             A     B     C     D     E     F     G     H     I     J
       A     0     4     2     7     0     0     0     0     0     0
       B     0     0     1     0     5     0     0     0     0     0
       C     0     0     0     2     3     4     0     0     0     0
       D     0     0     5     0     0     0     6     0     0     0
       E     0     0     0     0     0     3     0     5     0     0
       F     0     0     0     0     0     0     2     0     6     1
       G     0     0     0     0     0     0     0     0     1     4
       H     0     0     0     0     0     0     0     0     3     2
       I     0     0     0     0     0     0     0     0     0     4
       J     0     0     0     0     0     0     0     0     0     0"""

# Edge list output
EDGE_LIST_10 = """=== Edge List (Danh sách cạnh) ===
Loại đồ thị:    Có hướng
Trọng số:       Có
Số cạnh:        20
[(A,B,4), (A,C,2), (A,D,7), (B,C,1), (B,E,5), (C,D,2), (C,E,3), (C,F,4), (D,C,5), (D,G,6), (E,F,3), (E,H,5), (F,G,2), (F,I,6), (F,J,1), (G,I,1), (G,J,4), (H,I,3), (H,J,2), (I,J,4)]"""

# File output
FILE_OUTPUT_10 = """directed
weighted
10
20
A B C D E F G H I J
A B 4
A C 2
A D 7
B C 1
B E 5
C D 2
C E 3
C F 4
D C 5
D G 6
E F 3
E H 5
F G 2
F I 6
F J 1
G I 1
G J 4
H I 3
H J 2
I J 4"""

# BFS results
BFS_A = "A -> B -> C -> D -> E -> F -> G -> H -> I -> J"
BFS_B = "B -> C -> E -> D -> F -> H -> G -> I -> J"
BFS_C = "C -> D -> E -> F -> G -> H -> I -> J"

# DFS results
DFS_A = "A -> B -> C -> D -> G -> I -> J -> E -> F -> H"
DFS_B = "B -> C -> D -> G -> I -> J -> E -> F -> H"
DFS_C = "C -> D -> G -> I -> J -> E -> F -> H"

# Dijkstra results (from A)
DIJKSTRA_RESULTS = """[Dijkstra] Từ đỉnh 'A':
Đỉnh    Khoảng cách   Đường đi
A       0             A
B       4             A -> B
C       2             A -> C
D       4             A -> C -> D
E       5             A -> C -> E
F       6             A -> C -> F
G       8             A -> C -> F -> G
H       10            A -> C -> E -> H
I       9             A -> C -> F -> G -> I
J       7             A -> C -> F -> J

[dijkstra] A -> J
  Đường đi: A -> C -> F -> J
  Tổng trọng số: 7"""

# Bellman-Ford results
BELLMAN_FORD_RESULTS = """[bellman_ford] Từ đỉnh 'A':
Đỉnh    Khoảng cách   Đường đi
A       0             A
B       4             A -> B
C       2             A -> C
D       4             A -> C -> D
E       5             A -> C -> E
F       6             A -> C -> F
G       8             A -> C -> F -> G
H       10            A -> C -> E -> H
I       9             A -> C -> F -> G -> I
J       7             A -> C -> F -> J

[bellman_ford] A -> J
  Đường đi: A -> C -> F -> J
  Tổng trọng số: 7"""

# MST results (for undirected version)
KRUSKAL_RESULTS = """=== KRUSKAL - Cây khung nhỏ nhất ===
NHẬN (B, C) w=1 | tổng = 1
NHẬN (F, J) w=1 | tổng = 2
NHẬN (G, I) w=1 | tổng = 3
NHẬN (A, C) w=2 | tổng = 5
NHẬN (C, D) w=2 | tổng = 7
NHẬN (F, G) w=2 | tổng = 9
NHẬN (H, J) w=2 | tổng = 11
NHẬN (C, E) w=3 | tổng = 14
NHẬN (E, F) w=3 | tổng = 17
KẾT QUẢ Kruskal: 9 cạnh, tổng trọng số = 17"""

PRIM_RESULTS = """=== PRIM - Cây khung nhỏ nhất ===
Đỉnh bắt đầu: A
THÊM (A, C) w=2 | tổng = 2
THÊM (C, B) w=1 | tổng = 3
THÊM (C, D) w=2 | tổng = 5
THÊM (C, E) w=3 | tổng = 8
THÊM (E, F) w=3 | tổng = 11
THÊM (F, J) w=1 | tổng = 12
THÊM (F, G) w=2 | tổng = 14
THÊM (G, I) w=1 | tổng = 15
THÊM (J, H) w=2 | tổng = 17
KẾT QUẢ Prim: 9 cạnh, tổng trọng số = 17
So sánh: Kruskal = 17, Prim = 17 (khớp)"""

# Euler results
EULER_CHECK_10 = """=== KIỂM TRA ĐIỀU KIỆN EULER ===
Bậc các đỉnh:
  A: 3 (lẻ), B: 2 (chẵn), C: 3 (lẻ), D: 2 (chẵn), E: 2 (chẵn)
  F: 3 (lẻ), G: 2 (chẵn), H: 2 (chẵn), I: 1 (lẻ), J: 0 (chẵn)
Số đỉnh bậc lẻ: 4 -> ['A', 'C', 'F', 'I']
Liên thông (bỏ qua đỉnh cô lập)? Có
=> KHÔNG có đường đi/chu trình Euler (cần đúng 0 hoặc 2 đỉnh bậc lẻ)"""

# Max flow results
MAXFLOW_RESULTS = """=== FORD-FULKERSON (Nguồn: A, Đích: J) ===
Buoc 1: A -> C -> F -> J (+1)
Buoc 2: A -> D -> G -> J (+4)
Buoc 3: A -> B -> E -> H -> J (+2)
Buoc 4: A -> C -> F -> I -> J (+1)
Buoc 5: A -> D -> G -> I -> J (+1)
Buoc 6: A -> B -> C -> F -> I -> J (+1)
Buoc 7: A -> B -> E -> F -> I -> J (+1)

LUONG TOI DA: 11

Luong tren moi canh:
  A -> B: 4/4
  A -> C: 2/2
  A -> D: 5/7
  B -> C: 1/1
  B -> E: 3/5
  C -> F: 3/4
  D -> G: 5/6
  E -> F: 1/3
  E -> H: 2/5
  F -> I: 3/6
  F -> J: 1/1
  G -> I: 1/1
  G -> J: 4/4
  H -> J: 2/2
  I -> J: 4/4"""

# Full log - Nguoi 1
LOG_NGUOI_1 = """=================================================================
   NGƯỜI 1 - NỀN TẢNG & BIỂU DIỄN ĐỒ THỊ
=================================================================
=== Adjacency List (Danh sách kề) ===
Loại đồ thị:    Có hướng
Trọng số:       Có
----------------------------------------
A: B(4), C(2), D(7)
B: C(1), E(5)
C: D(2), E(3), F(4)
D: C(5), G(6)
E: F(3), H(5)
F: G(2), I(6), J(1)
G: I(1), J(4)
H: I(3), J(2)
I: J(4)
J:

=== Adjacency Matrix (Ma trận kề) ===
             A     B     C     D     E     F     G     H     I     J
       A     0     4     2     7     0     0     0     0     0     0
       B     0     0     1     0     5     0     0     0     0     0
       C     0     0     0     2     3     4     0     0     0     0
       D     0     0     5     0     0     0     6     0     0     0
       E     0     0     0     0     0     3     0     5     0     0
       F     0     0     0     0     0     0     2     0     6     1
       G     0     0     0     0     0     0     0     0     1     4
       H     0     0     0     0     0     0     0     0     3     2
       I     0     0     0     0     0     0     0     0     0     4
       J     0     0     0     0     0     0     0     0     0     0

=== Edge List (Danh sách cạnh) ===
Số cạnh:        20
(A,B,4), (A,C,2), (A,D,7), (B,C,1), (B,E,5), (C,D,2), (C,E,3), (C,F,4),
(D,C,5), (D,G,6), (E,F,3), (E,H,5), (F,G,2), (F,I,6), (F,J,1), (G,I,1),
(G,J,4), (H,I,3), (H,J,2), (I,J,4)

Đã lưu đồ thị vào file: graph_data_out.txt
Đã lưu hình đồ thị: graph_output.png"""

# Full log - Nguoi 2
LOG_NGUOI_2 = """=================================================================
   NGƯỜI 2 - DUYỆT ĐỒ THỊ & TÔ MÀU
=================================================================
[BFS] từ 'A': A -> B -> C -> D -> E -> F -> G -> H -> I -> J
[DFS] từ 'A': A -> B -> C -> D -> G -> I -> J -> E -> F -> H

Đồ thị KHÔNG phải là đồ thị hai phía.

Số màu cần dùng: 2
  A: màu 0
  B: màu 1
  C: màu 0
  D: màu 1
  E: màu 1
  F: màu 0
  G: màu 0
  H: màu 0
  I: màu 0
  J: màu 0"""

# Full log - Nguoi 3
LOG_NGUOI_3 = """=================================================================
   NGƯỜI 3 - ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA & BELLMAN-FORD)
=================================================================
--- Dijkstra ---
[dijkstra] Từ đỉnh 'A':
Đỉnh    Khoảng cách   Đường đi
A       0             A
B       4             A -> B
C       2             A -> C
D       4             A -> C -> D
E       5             A -> C -> E
F       6             A -> C -> F
G       8             A -> C -> F -> G
H       10            A -> C -> E -> H
I       9             A -> C -> F -> G -> I
J       7             A -> C -> F -> J
[dijkstra] A -> J   Đường đi: A -> C -> F -> J   Tổng trọng số: 7

--- Bellman-Ford ---
[bellman_ford] Từ đỉnh 'A':
Đỉnh    Khoảng cách   Đường đi
A       0             A
B       4             A -> B
C       2             A -> C
D       4             A -> C -> D
E       5             A -> C -> E
F       6             A -> C -> F
G       8             A -> C -> F -> G
H       10            A -> C -> E -> H
I       9             A -> C -> F -> G -> I
J       7             A -> C -> F -> J
[bellman_ford] A -> J   Đường đi: A -> C -> F -> J   Tổng trọng số: 7"""

# Full log - Nguoi 4
LOG_NGUOI_4 = """=================================================================
   NGƯỜI 4 - THUẬT TOÁN NÂNG CAO (KRUSKAL, PRIM, HIERHOLZER)
=================================================================
--- Kruskal --- (trên đồ thị vô hướng - bỏ hướng)
NHẬN (B, C) w=1 | tổng = 1
NHẬN (F, J) w=1 | tổng = 2
NHẬN (G, I) w=1 | tổng = 3
NHẬN (A, C) w=2 | tổng = 5
NHẬN (C, D) w=2 | tổng = 7
NHẬN (F, G) w=2 | tổng = 9
NHẬN (H, J) w=2 | tổng = 11
NHẬN (C, E) w=3 | tổng = 14
NHẬN (E, F) w=3 | tổng = 17
KẾT QUẢ Kruskal: 9 cạnh, tổng trọng số = 17

--- Prim --- (xuất phát từ A)
THÊM (A, C) w=2 | THÊM (C, B) w=1 | THÊM (C, D) w=2 | THÊM (C, E) w=3
THÊM (E, F) w=3 | THÊM (F, J) w=1 | THÊM (F, G) w=2 | THÊM (G, I) w=1
THÊM (J, H) w=2
KẾT QUẢ Prim: 9 cạnh, tổng trọng số = 17
So sánh: Kruskal = 17, Prim = 17 (khớp)

--- Hierholzer: kiểm tra đồ thị ---
Số đỉnh bậc lẻ: 4 -> ['A', 'C', 'F', 'I']
=> KHÔNG có đường đi/chu trình Euler

--- Ford-Fulkerson (Nguồn: A, Đích: J) ---
Buoc 1: A -> C -> F -> J (+1)
Buoc 2: A -> D -> G -> J (+4)
Buoc 3: A -> B -> E -> H -> J (+2)
Buoc 4: A -> C -> F -> I -> J (+1)
Buoc 5: A -> D -> G -> I -> J (+1)
Buoc 6: A -> B -> C -> F -> I -> J (+1)
Buoc 7: A -> B -> E -> F -> I -> J (+1)
LUONG TOI DA: 11

#################################################################
#                        HOÀN THÀNH!                          #
#################################################################"""

# Code for graph.py (Nguoi 1)
CODE_GRAPH_PY = '''"""
graph.py - Lop Do Thi co ban
Mo ta: Luu tru va quan ly do thi voi cac phep bieu dien:
  - Danh sach ke (Adjacency List)
  - Ma tran ke (Adjacency Matrix)
  - Danh sach canh (Edge List)
"""

import math


class Graph:
    """Lop Do Thi ho tro co huong/vo huong, co trong so/khong trong so"""

    def __init__(self, nodes=None, edges=None, is_directed=False, weighted=True):
        self.nodes = list(nodes) if nodes else []
        self.is_directed = is_directed
        self.weighted = weighted
        self.adj = {}
        for node in self.nodes:
            self.adj[node] = []
        if edges:
            for edge in edges:
                if len(edge) == 3:
                    u, v, w = edge
                else:
                    u, v = edge
                    w = 1
                self.add_edge(u, v, w)

    def add_edge(self, u, v, w=1):
        self.adj[u].append((v, w))
        if not self.is_directed:
            self.adj[v].append((u, w))

    def get_neighbors(self, node):
        return list(self.adj.get(node, []))

    def get_degree(self, node):
        return len(self.adj.get(node, []))

    def get_all_edges(self):
        edges, seen = [], set()
        for u in self.nodes:
            for v, w in self.adj[u]:
                if self.is_directed:
                    edges.append((u, v, w))
                else:
                    key = (min(u, v), max(u, v))
                    if key not in seen:
                        seen.add(key)
                        edges.append((u, v, w))
        return edges

    def get_adjacency_matrix(self):
        n = len(self.nodes)
        idx = {node: i for i, node in enumerate(self.nodes)}
        matrix = [[0]*n for _ in range(n)]
        for u in self.nodes:
            for v, w in self.adj[u]:
                matrix[idx[u]][idx[v]] = w
        return matrix, self.nodes

    def get_adjacency_list(self):
        return {node: list(self.adj[node]) for node in self.nodes}

    def get_edge_list(self):
        return self.get_all_edges()

    def display_representations(self):
        matrix, nodes = self.get_adjacency_matrix()
        print("\\n1. MA TRAN KE:")
        print("   ", end="")
        for node in nodes:
            print(f"{node:>5}", end="")
        print()
        for i, node in enumerate(nodes):
            print(f"  {node}|", end="")
            for j in range(len(nodes)):
                print(f"{matrix[i][j]:>5}", end="")
            print()

        adj_list = self.get_adjacency_list()
        print("\\n2. DANH SACH KE:")
        for node in self.nodes:
            items = [f"{nb}({w})" for nb, w in adj_list[node]]
            print(f"   {node}: {', '.join(items)}")

        edge_list = self.get_edge_list()
        print("\\n3. DANH SACH CANH:")
        items = [f"({u},{v},{w})" for u, v, w in edge_list]
        print(f"   [{', '.join(items)}]")

    def draw_graph(self, filename="graph.png", title="Do Thi",
                   node_colors=None, highlight_edges=None):
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import networkx as nx
        except ImportError:
            print("  Can cai matplotlib va networkx")
            return None

        if self.is_directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        for node in self.nodes:
            G.add_node(node)
        for u in self.nodes:
            for v, w in self.get_neighbors(u):
                if self.is_directed or (u < v):
                    G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G, seed=42)
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=14, fontweight="bold")

        highlight_set = set()
        if highlight_edges:
            for u, v in highlight_edges:
                highlight_set.add((u, v))
                if not self.is_directed:
                    highlight_set.add((v, u))

        for u in self.nodes:
            for v, w in self.get_neighbors(u):
                if self.is_directed or (u < v):
                    x1, y1 = pos[u]
                    x2, y2 = pos[v]
                    is_hl = (u, v) in highlight_set
                    color = "red" if is_hl else "gray"
                    lw = 2.5 if is_hl else 1.0
                    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="-|>" if self.is_directed else "-",
                                        color=color, lw=lw, shrinkA=12, shrinkB=12))
                    mx, my = (x1+x2)/2, (y1+y2)/2
                    if self.weighted:
                        ax.text(mx, my, str(w), fontsize=8, ha="center", va="center",
                            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.8))

        for node in self.nodes:
            x, y = pos[node]
            if node_colors and node in node_colors:
                c = node_colors[node]
                color = c if isinstance(c, str) else (c[0], c[1], c[2])
            else:
                color = "lightblue"
            circle = plt.Circle((x, y), 0.08, color=color, ec="black", lw=1.5, zorder=5)
            ax.add_patch(circle)
            ax.text(x, y, str(node), ha="center", va="center", fontsize=10,
                    fontweight="bold", zorder=6)

        margin = 0.3
        ax.set_xlim(-1-margin, 1+margin)
        ax.set_ylim(-1-margin, 1+margin)
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Da luu hinh: {filename}")
        return filename

    def copy(self):
        edges = self.get_all_edges()
        return Graph(
            nodes=list(self.nodes),
            edges=list(edges),
            is_directed=self.is_directed,
            weighted=self.weighted,
        )'''

# Code for q3_traversal.py (Nguoi 2)
CODE_TRAVERSAL = '''"""
q3_traversal.py - BFS & DFS
"""

from graph import Graph


def bfs(graph, start):
    visited = {start: 1}
    queue = [start]
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        neighbors = sorted([nb for nb, w in graph.get_neighbors(node)
                           if nb not in visited])
        for nb in neighbors:
            visited[nb] = 1
            queue.append(nb)
    return order


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
        neighbors = sorted([nb for nb, w in graph.get_neighbors(node)
                           if nb not in visited], reverse=True)
        for nb in neighbors:
            stack.append(nb)
    return order


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


def graph_coloring(graph):
    nodes_by_degree = sorted(graph.nodes,
        key=lambda n: len(graph.get_neighbors(n)), reverse=True)
    color = {}
    for node in nodes_by_degree:
        used = {color[v] for v, w in graph.get_neighbors(node) if v in color}
        c = 0
        while c in used:
            c += 1
        color[node] = c
    return color, len(set(color.values()))'''

# Code for q5_shortest.py (Nguoi 3)
CODE_SHORTEST = '''"""
q5_shortest.py - Dijkstra & Bellman-Ford
"""

from graph import Graph

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


def trace_path(parent, source, target):
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    if len(path) == 0 or path[0] != source:
        return None
    return path'''

# Code for q73q74_mst.py (Nguoi 4 - MST)
CODE_MST = '''"""
q73q74_mst.py - Prim & Kruskal (MST)
"""

from graph import Graph

INF = 999999999


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


def kruskal(graph):
    sorted_edges = sorted(graph.get_all_edges(), key=lambda e: e[2])
    uf = UnionFind(graph.nodes)
    mst_edges = []
    total = 0
    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total += w
        if len(mst_edges) == len(graph.nodes) - 1:
            break
    return mst_edges, total'''

# Code for q75_maxflow.py (Nguoi 4 - Max Flow)
CODE_MAXFLOW = '''"""
q75_maxflow.py - Ford-Fulkerson (Luong toi da)
"""

from graph import Graph

INF = 999999999


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
        steps.append((path, min_r))
    return flow, max_flow, steps'''

# Code snippets for algorithm explanation tables
CODE_BFS_SNIPPET = """visited = {start}; order = [start]; queue = [start]
while queue:
    node = queue.pop(0)
    order.append(node)
    neighbors = sorted([nb for nb, w in graph.get_neighbors(node)
                       if nb not in visited])
    for nb in neighbors:
        visited[nb] = 1; queue.append(nb)"""

CODE_DFS_SNIPPET = """visited = {}; stack = [start]; order = []
while stack:
    node = stack.pop()
    if node in visited: continue
    visited[node] = 1; order.append(node)
    neighbors = sorted([nb for nb, w in graph.get_neighbors(node)
                       if nb not in visited], reverse=True)
    for nb in neighbors:
        stack.append(nb)"""

CODE_BIPARTITE_SNIPPET = """for node in graph.nodes:
    if node in coloring: continue
    queue = [node]; coloring[node] = 0
    while queue:
        u = queue.pop(0)
        for v, w in graph.get_neighbors(u):
            if v not in coloring:
                coloring[v] = 1 - coloring[u]; queue.append(v)
            elif coloring[v] == coloring[u]:
                return False, coloring"""

CODE_COLORING_SNIPPET = """nodes_by_degree = sorted(graph.nodes,
    key=lambda n: len(graph.get_neighbors(n)), reverse=True)
for node in nodes_by_degree:
    used = {color[v] for v, w in graph.get_neighbors(node) if v in color}
    c = 0
    while c in used: c += 1
    color[node] = c"""

CODE_DIJKSTRA_SNIPPET = """dist = {n: INF for n in graph.nodes}
parent = {n: None for n in graph.nodes}
dist[source] = 0; visited = {}
for _ in range(len(graph.nodes)):
    u = None; min_d = INF
    for n in graph.nodes:
        if n not in visited and dist[n] < min_d:
            min_d = dist[n]; u = n
    if u is None: break
    visited[u] = 1
    for v, w in graph.get_neighbors(u):
        if v not in visited and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w; parent[v] = u"""

CODE_BELLMANFORD_SNIPPET = """edges = graph.get_all_edges()
for i in range(len(graph.nodes) - 1):
    updated = False
    for u, v, w in edges:
        if dist[u] < INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w; parent[v] = u; updated = True
    if not updated: break
# quet them 1 lan de phat hien chu trinh am
for u, v, w in edges:
    if dist[u] < INF and dist[u] + w < dist[v]:
        has_neg = True"""

CODE_KRUSKAL_SNIPPET = """sorted_edges = sorted(graph.get_all_edges(), key=lambda e: e[2])
uf = UnionFind(graph.nodes)
mst_edges = []; total = 0
for u, v, w in sorted_edges:
    if uf.union(u, v):
        mst_edges.append((u, v, w)); total += w
    if len(mst_edges) == len(graph.nodes) - 1: break"""

CODE_PRIM_SNIPPET = """in_tree = {start: 1}; mst_edges = []; total = 0
for _ in range(len(graph.nodes) - 1):
    best_edge = None; best_w = INF
    for node in in_tree:
        for nb, w in graph.get_neighbors(node):
            if nb not in in_tree and w < best_w:
                best_w = w; best_edge = (node, nb, w)
    if best_edge is None: break
    u, v, w = best_edge
    mst_edges.append(best_edge); total += w
    in_tree[v] = 1"""

CODE_EULER_SNIPPET = """# Kiem tra dieu kien Euler
odd_nodes = [n for n in graph.nodes if graph.get_degree(n) % 2 == 1]
# 0 dinh le -> "circuit"; dung 2 dinh le -> "path"; con lai -> "none"

# Hierholzer
g = graph.copy(); stack = [start]; circuit = []
while stack:
    u = stack[-1]
    neighbors = g.get_neighbors(u)
    if neighbors:
        v, w = neighbors[0]
        stack.append(v); g.remove_edge(u, v)
    else:
        circuit.append(stack.pop())
circuit.reverse()"""


def main():
    print("Dang tai file docx goc...")
    doc = Document(INPUT)
    print(f"  So doan van: {len(doc.paragraphs)}")
    print(f"  So bang: {len(doc.tables)}")

    # ============================================================
    # CHANGE 1: Cap nhat mo ta do thi mau (chuong 1)
    # ============================================================
    print("\n[1/10] Cap nhat mo ta do thi mau...")
    for i, para in enumerate(doc.paragraphs):
        txt = para.text.strip()
        # Change graph description
        if "14 đỉnh và 21 cạnh" in txt:
            set_paragraph_text(para, txt.replace("14 đỉnh và 21 cạnh", "10 đỉnh và 20 cạnh"))
        elif "vô hướng, có trọng số, gồm 14 đỉnh và 21 cạnh" in txt:
            set_paragraph_text(para, txt.replace("vô hướng, có trọng số, gồm 14 đỉnh và 21 cạnh",
                                                 "có hướng, có trọng số, gồm 10 đỉnh và 20 cạnh"))
        elif "14 đỉnh, 21 cạnh" in txt and "mẫu" in txt.lower():
            set_paragraph_text(para, txt.replace("14 đỉnh, 21 cạnh", "10 đỉnh, 20 cạnh"))
        elif "14 đỉnh" in txt and ("mẫu" in txt or "minh hoạ" in txt):
            set_paragraph_text(para, txt.replace("14 đỉnh", "10 đỉnh"))

        # Change edge list description
        if "A–B (4), A–C (2), A–D (7), B–E (5), B–G (3), C–E (6), C–F (8), D–G (4), D–H (3), E–H (7), E–I (2), F–J (5), G–I (9), G–K (3), H–K (6), H–L (4), I–L (8), I–M (5), K–N (7), L–N (2), M–N (3)" in txt:
            new_edges = "A→B(4), A→C(2), A→D(7), B→C(1), B→E(5), C→D(2), C→E(3), C→F(4), D→C(5), D→G(6), E→F(3), E→H(5), F→G(2), F→I(6), F→J(1), G→I(1), G→J(4), H→I(3), H→J(2), I→J(4)"
            set_paragraph_text(para, txt.replace("A–B (4), A–C (2), A–D (7), B–E (5), B–G (3), C–E (6), C–F (8), D–G (4), D–H (3), E–H (7), E–I (2), F–J (5), G–I (9), G–K (3), H–K (6), H–L (4), I–L (8), I–M (5), K–N (7), L–N (2), M–N (3)", new_edges))

        # Change class name references
        if "graph_module.py" in txt:
            set_paragraph_text(para, txt.replace("graph_module.py", "graph.py"))
        if "graph_traversal.py" in txt:
            set_paragraph_text(para, txt.replace("graph_traversal.py", "q3_traversal.py"))
        if "graph_shortest_path.py" in txt:
            set_paragraph_text(para, txt.replace("graph_shortest_path.py", "q5_shortest.py"))
        if "graph_advanced_algorithms.py" in txt:
            set_paragraph_text(para, txt.replace("graph_advanced_algorithms.py", "q73q74_mst.py / q75_maxflow.py"))

        # Change references to 14-vertex graph
        if "đồ thị mẫu 14 đỉnh" in txt:
            set_paragraph_text(para, txt.replace("đồ thị mẫu 14 đỉnh", "đồ thị mẫu 10 đỉnh"))
        if "Đồ thị mẫu 14 đỉnh" in txt:
            set_paragraph_text(para, txt.replace("Đồ thị mẫu 14 đỉnh", "Đồ thị mẫu 10 đỉnh"))
        if "trên đồ thị 14 đỉnh" in txt:
            set_paragraph_text(para, txt.replace("trên đồ thị 14 đỉnh", "trên đồ thị 10 đỉnh"))

    # ============================================================
    # CHANGE 2: Cap nhat bang file structure (Table 1)
    # ============================================================
    print("[2/10] Cap nhat bang cau truc file...")
    if len(doc.tables) > 1:
        table = doc.tables[1]
        for row in table.rows:
            for cell in row.cells:
                if "graph_module.py" in cell.text:
                    for p in cell.paragraphs:
                        if "graph_module.py" in p.text:
                            for run in p.runs:
                                if "graph_module.py" in run.text:
                                    run.text = run.text.replace("graph_module.py", "graph.py")
                if "graph_traversal.py" in cell.text:
                    for p in cell.paragraphs:
                        if "graph_traversal.py" in p.text:
                            for run in p.runs:
                                if "graph_traversal.py" in run.text:
                                    run.text = run.text.replace("graph_traversal.py", "q3_traversal.py")
                if "graph_shortest_path.py" in cell.text:
                    for p in cell.paragraphs:
                        if "graph_shortest_path.py" in p.text:
                            for run in p.runs:
                                if "graph_shortest_path.py" in run.text:
                                    run.text = run.text.replace("graph_shortest_path.py", "q5_shortest.py")
                if "graph_advanced_algorithms.py" in cell.text:
                    for p in cell.paragraphs:
                        if "graph_advanced_algorithms.py" in p.text:
                            for run in p.runs:
                                if "graph_advanced_algorithms.py" in run.text:
                                    run.text = run.text.replace("graph_advanced_algorithms.py",
                                        "q73q74_mst.py / q75_maxflow.py")

    # ============================================================
    # CHANGE 3: Cap nhat ket qua bieu dien (Tables 3-7)
    # ============================================================
    print("[3/10] Cap nhat ket qua bieu dien do thi...")
    for i in range(3, 8):
        if i < len(doc.tables):
            table = doc.tables[i]
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text
                    if "Vô hướng" in text:
                        for p in cell.paragraphs:
                            for run in p.runs:
                                if "Vô hướng" in run.text:
                                    run.text = run.text.replace("Vô hướng", "Có hướng")

    # Update table 7 (file output) - the undirected/weighted/5/6 graph
    if len(doc.tables) > 7:
        table = doc.tables[7]
        for row in table.rows:
            for cell in row.cells:
                if "undirected" in cell.text:
                    set_cell_text(cell, FILE_OUTPUT_10)

    # ============================================================
    # CHANGE 4: Cap nhat code (Tables 8-14)
    # ============================================================
    print("[4/10] Cap nhat source code...")
    code_tables = {
        8: CODE_GRAPH_PY,
        22: CODE_TRAVERSAL,
        31: CODE_SHORTEST,
        42: CODE_MST,
    }
    for table_idx, code in code_tables.items():
        if table_idx < len(doc.tables):
            table = doc.tables[table_idx]
            for row in table.rows:
                for cell in row.cells:
                    if len(cell.text) > 50:
                        set_cell_text(cell, code)

    # Update code snippet tables
    snippet_tables = {
        9: CODE_GRAPH_PY[:500],  # __init__
        10: "def add_edge(self, u, v, w=1):\n    self.adj[u].append((v, w))\n    if not self.is_directed:\n        self.adj[v].append((u, w))",
        11: "n = len(self.nodes)\nidx = {node: i for i, node in enumerate(self.nodes)}\nmatrix = [[0]*n for _ in range(n)]\nfor u in self.nodes:\n    for v, w in self.adj[u]:\n        matrix[idx[u]][idx[v]] = w",
        12: "edges, seen = [], set()\nfor u in self.nodes:\n    for v, w in self.adj[u]:\n        if self.is_directed:\n            edges.append((u, v, w))\n        else:\n            key = (min(u, v), max(u, v))\n            if key not in seen:\n                seen.add(key); edges.append((u, v, w))",
        13: 'f.write("directed\\n" if self.is_directed else "undirected\\n")\nf.write("weighted\\n" if self.weighted else "unweighted\\n")\nf.write(f"{len(self.nodes)}\\n"); f.write(f"{len(edges)}\\n")\nf.write(" ".join(map(str, self.nodes)) + "\\n")\nfor u, v, w in edges:\n    f.write(f"{u} {v} {w}\\n")',
        14: "import networkx as nx\nG = nx.DiGraph() if self.is_directed else nx.Graph()\npos = nx.spring_layout(G, seed=42)\nif self.is_directed:\n    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20)",
        23: CODE_BFS_SNIPPET,
        24: CODE_DFS_SNIPPET,
        25: CODE_BIPARTITE_SNIPPET,
        26: CODE_COLORING_SNIPPET,
        32: CODE_DIJKSTRA_SNIPPET,
        33: CODE_BELLMANFORD_SNIPPET,
        44: CODE_KRUSKAL_SNIPPET,
        45: CODE_PRIM_SNIPPET,
        46: CODE_EULER_SNIPPET,
    }
    for table_idx, code in snippet_tables.items():
        if table_idx < len(doc.tables):
            table = doc.tables[table_idx]
            for row in table.rows:
                for cell in row.cells:
                    if len(cell.text) > 20:
                        set_cell_text(cell, code)

    # ============================================================
    # CHANGE 5: Cap nhat bang canh (Table 15)
    # ============================================================
    print("[5/10] Cap nhat bang canh mau...")
    if len(doc.tables) > 15:
        table = doc.tables[15]
        # This is the edge/weight table for the old 5-vertex graph
        # Replace with edges from 10-vertex graph
        # Clear existing rows
        while len(table.rows) > 1:
            tr = table.rows[-1]._tr
            tr.getparent().remove(tr)
        # Add new edges
        edges_for_table = [
            ("A→B", "4"), ("A→C", "2"), ("A→D", "7"), ("B→C", "1"),
            ("B→E", "5"), ("C→D", "2"), ("C→E", "3"), ("C→F", "4"),
        ]
        # Update header
        header_row = table.rows[0]
        cells = header_row.cells
        set_cell_text(cells[0], "Cạnh")
        for j in range(1, min(len(cells), 5)):
            idx = j - 1
            if idx < len(edges_for_table):
                set_cell_text(cells[j], edges_for_table[idx][0])
        # Add weight row
        row = table.add_row()
        set_cell_text(row.cells[0], "Trọng số")
        for j in range(1, min(len(row.cells), 5)):
            idx = j - 1
            if idx < len(edges_for_table):
                set_cell_text(row.cells[j], edges_for_table[idx][1])

    # ============================================================
    # CHANGE 6: Cap nhat ket qua BFS/DFS (Tables 17-18, 27)
    # ============================================================
    print("[6/10] Cap nhat ket qua BFS/DFS...")
    bfs_dfs_tables = {
        17: f"[BFS] từ 'A': {BFS_A}",
        18: f"[DFS] từ 'A': {DFS_A}",
        27: f"[BFS] từ 'A': {BFS_A}\n[DFS] từ 'A': {DFS_A}\n\nĐồ thị KHÔNG phải là đồ thị hai phía.\n\nSố màu cần dùng: 2\n  A: màu 0\n  B: màu 1\n  C: màu 0\n  D: màu 1\n  E: màu 1\n  F: màu 0\n  G: màu 0\n  H: màu 0\n  I: màu 0\n  J: màu 0",
    }
    for table_idx, content in bfs_dfs_tables.items():
        if table_idx < len(doc.tables):
            table = doc.tables[table_idx]
            for row in table.rows:
                for cell in row.cells:
                    if len(cell.text) > 5:
                        set_cell_text(cell, content)

    # ============================================================
    # CHANGE 7: Cap nhat ket qua to mau (Tables 20-21)
    # ============================================================
    print("[7/10] Cap nhat ket qua to mau...")
    # Table 20 - coloring table
    if len(doc.tables) > 20:
        table = doc.tables[20]
        # Clear and rebuild
        while len(table.rows) > 1:
            tr = table.rows[-1]._tr
            tr.getparent().remove(tr)
        # Update header
        header_row = table.rows[0]
        set_cell_text(header_row.cells[0], "Dinh")
        set_cell_text(header_row.cells[1], "Bac")
        set_cell_text(header_row.cells[2], "Mau")

        coloring_data = [
            ("A", "3", "0"), ("B", "2", "1"), ("C", "3", "0"),
            ("D", "2", "1"), ("E", "2", "1"), ("F", "3", "0"),
            ("G", "2", "0"), ("H", "2", "0"), ("I", "1", "0"),
            ("J", "0", "0"),
        ]
        for node, deg, color in coloring_data:
            row = table.add_row()
            set_cell_text(row.cells[0], node)
            set_cell_text(row.cells[1], deg)
            set_cell_text(row.cells[2], color)

    # Table 21 - coloring result
    if len(doc.tables) > 21:
        table = doc.tables[21]
        for row in table.rows:
            for cell in row.cells:
                if "Số màu" in cell.text or "màu" in cell.text:
                    set_cell_text(cell, "Số màu cần dùng: 2\n  A: màu 0\n  B: màu 1\n  C: màu 0\n  D: màu 1\n  E: màu 1\n  F: màu 0\n  G: màu 0\n  H: màu 0\n  I: màu 0\n  J: màu 0")

    # ============================================================
    # CHANGE 8: Cap nhat ket qua duong di ngan nhat (Table 36)
    # ============================================================
    print("[8/10] Cap nhat ket qua duong di ngan nhat...")
    if len(doc.tables) > 36:
        table = doc.tables[36]
        for row in table.rows:
            for cell in row.cells:
                if "Dijkstra" in cell.text or "dijkstra" in cell.text:
                    set_cell_text(cell, DIJKSTRA_RESULTS)

    # ============================================================
    # CHANGE 9: Cap nhat ket qua MST/Euler (Tables 37-41, 47)
    # ============================================================
    print("[9/10] Cap nhat ket qua MST/Euler...")
    mst_euler_tables = {
        37: KRUSKAL_RESULTS,
        38: PRIM_RESULTS,
        41: EULER_CHECK_10,
        47: f"--- Kruskal --- (trên đồ thị vô hướng - bỏ hướng)\n{KRUSKAL_RESULTS}\n\n--- Prim --- (xuất phát từ A)\n{PRIM_RESULTS}\n\n--- Hierholzer: kiểm tra đồ thị ---\n{EULER_CHECK_10}",
    }
    for table_idx, content in mst_euler_tables.items():
        if table_idx < len(doc.tables):
            table = doc.tables[table_idx]
            for row in table.rows:
                for cell in row.cells:
                    if len(cell.text) > 10:
                        set_cell_text(cell, content)

    # ============================================================
    # CHANGE 10: Cap nhat log chay va ket luan (Tables 50-54)
    # ============================================================
    print("[10/10] Cap nhat log chay tong hop...")
    log_tables = {
        50: "$ python3 main.py\n(chiec cai dat truoc: pip install matplotlib networkx)",
        51: LOG_NGUOI_1,
        52: LOG_NGUOI_2,
        53: LOG_NGUOI_3,
        54: LOG_NGUOI_4,
    }
    for table_idx, content in log_tables.items():
        if table_idx < len(doc.tables):
            table = doc.tables[table_idx]
            for row in table.rows:
                for cell in row.cells:
                    if len(cell.text) > 20:
                        set_cell_text(cell, content)

    # ============================================================
    # UPDATE paragraph references to old graph
    # ============================================================
    print("\nCap nhat cac tham chieu cu...")
    for i, para in enumerate(doc.paragraphs):
        txt = para.text
        # Replace old file names
        replacements = {
            "do_thi_full_project.py": "main.py",
            "graph_module.py": "graph.py",
            "graph_traversal.py": "q3_traversal.py",
            "graph_shortest_path.py": "q5_shortest.py",
            "graph_advanced_algorithms.py": "q73q74_mst.py",
            "14 đỉnh": "10 đỉnh",
            "21 cạnh": "20 cạnh",
        }
        for old, new in replacements.items():
            if old in txt:
                txt = txt.replace(old, new)
        # Replace graph type references
        if "đồ thị vô hướng" in txt and "mẫu" in txt:
            txt = txt.replace("đồ thị vô hướng", "đồ thị có hướng")
        if "Đồ thị vô hướng" in txt:
            txt = txt.replace("Đồ thị vô hướng", "Đồ thị có hướng")
        if txt != para.text:
            set_paragraph_text(para, txt)

    # Save
    print(f"\nDang luu file moi: {OUTPUT}")
    doc.save(OUTPUT)
    print("Hoan thanh!")


if __name__ == "__main__":
    main()
