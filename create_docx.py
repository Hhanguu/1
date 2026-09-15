"""
create_docx.py - Tao file docx bang ket qua chi tiet
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn


def set_cell_shading(cell, color):
    shading_elm = cell._element.get_or_add_tcPr()
    shd = shading_elm.makeelement(qn('w:shd'), {
        qn('w:fill'): color,
        qn('w:val'): 'clear'
    })
    shading_elm.append(shd)


def add_table_row(table, cells, bold=False, header=False):
    row = table.add_row()
    for i, text in enumerate(cells):
        cell = row.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(str(text))
        run.font.size = Pt(10)
        if bold or header:
            run.bold = True
        if header:
            set_cell_shading(cell, "4472C4")
            run.font.color.rgb = RGBColor(255, 255, 255)
    return row


def create_docx():
    doc = Document()

    # ===== TITLE =====
    title = doc.add_heading("BANG TONG HOP KET QUA", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("Do thi mau 10 dinh A-J — 21 canh, co huong, co trong so")
    run.font.size = Pt(14)
    run.bold = True

    doc.add_paragraph()

    # ===== DO THI MAU =====
    doc.add_heading("1. Do thi mau", level=1)
    doc.add_paragraph("Do thi co huong, co trong so, 10 dinh (A-J), 20 canh.")

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

    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["#", "Canh", "Trong so"], header=True)
    for i, (u, v, w) in enumerate(edges, 1):
        add_table_row(table, [str(i), f"{u} -> {v}", str(w)])

    doc.add_paragraph()

    # ===== CHUONG I-II: BIEU DIEN =====
    doc.add_heading("2. Chuong I-II: Cac phep bieu dien do thi", level=1)

    # Ma tran ke
    doc.add_heading("2.1 Ma tran ke (Adjacency Matrix)", level=2)
    nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    matrix = [
        [0, 4, 2, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 3, 4, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 6, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 3, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    table = doc.add_table(rows=1, cols=11)
    table.style = 'Table Grid'
    add_table_row(table, [""] + nodes, header=True)
    for i, node in enumerate(nodes):
        row_data = [node] + [str(x) for x in matrix[i]]
        add_table_row(table, row_data)

    doc.add_paragraph()

    # Danh sach ke
    doc.add_heading("2.2 Danh sach ke (Adjacency List)", level=2)
    adj_list = {
        "A": "B(4), C(2), D(7)",
        "B": "C(1), E(5)",
        "C": "D(2), E(3), F(4)",
        "D": "C(5), G(6)",
        "E": "F(3), H(5)",
        "F": "G(2), I(6), J(1)",
        "G": "I(1), J(4)",
        "H": "I(3), J(2)",
        "I": "J(4)",
        "J": "",
    }

    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    add_table_row(table, ["Dinh", "Danh sach ke"], header=True)
    for node in nodes:
        add_table_row(table, [node, adj_list[node]])

    doc.add_paragraph()

    # Danh sach canh
    doc.add_heading("2.3 Danh sach canh (Edge List)", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["#", "Canh", "Trong so"], header=True)
    for i, (u, v, w) in enumerate(edges, 1):
        add_table_row(table, [str(i), f"({u}, {v})", str(w)])

    doc.add_paragraph()

    # ===== CODE Q1Q2 =====
    doc.add_heading("2.4 Code - Bieu dien do thi (graph.py)", level=2)
    code_repr = '''class Graph:
    def __init__(self, nodes=None, edges=None, is_directed=False, weighted=True):
        self.nodes = list(nodes) if nodes else []
        self.is_directed = is_directed
        self.weighted = weighted
        self.adj = {}
        for node in self.nodes:
            self.adj[node] = []
        if edges:
            for edge in edges:
                u, v, w = edge if len(edge) == 3 else (edge[0], edge[1], 1)
                self.add_edge(u, v, w)

    def add_edge(self, u, v, w=1):
        self.adj[u].append((v, w))
        if not self.is_directed:
            self.adj[v].append((u, w))

    def get_neighbors(self, node):
        return list(self.adj.get(node, []))

    def get_adjacency_matrix(self):
        n = len(self.nodes)
        idx = {node: i for i, node in enumerate(self.nodes)}
        matrix = [[0]*n for _ in range(n)]
        for u in self.nodes:
            for v, w in self.adj[u]:
                matrix[idx[u]][idx[v]] = w
        return matrix, self.nodes

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
        return edges'''
    doc.add_paragraph(code_repr, style='Normal')
    doc.add_paragraph()

    # ===== CHUONG III: BFS & DFS =====
    doc.add_heading("3. Chuong III: Duyet BFS & DFS", level=1)

    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Dinh bat dau", "BFS", "DFS"], header=True)
    bfs_results = {
        "A": "A -> B -> C -> D -> E -> F -> G -> H -> I -> J",
        "B": "B -> C -> E -> D -> F -> H -> G -> I -> J",
        "C": "C -> D -> E -> F -> G -> H -> I -> J",
    }
    dfs_results = {
        "A": "A -> B -> C -> D -> G -> I -> J -> E -> F -> H",
        "B": "B -> C -> D -> G -> I -> J -> E -> F -> H",
        "C": "C -> D -> G -> I -> J -> E -> F -> H",
    }
    for s in ["A", "B", "C"]:
        add_table_row(table, [s, bfs_results[s], dfs_results[s]])

    doc.add_paragraph()

    # Code BFS
    doc.add_heading("3.1 Code BFS", level=2)
    code_bfs = '''def bfs(graph, start):
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
    return order'''
    doc.add_paragraph(code_bfs, style='Normal')

    # Code DFS
    doc.add_heading("3.2 Code DFS", level=2)
    code_dfs = '''def dfs(graph, start):
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
    return order'''
    doc.add_paragraph(code_dfs, style='Normal')

    # So sanh BFS vs DFS
    doc.add_heading("3.3 So sanh BFS vs DFS", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Tieu chi", "BFS", "DFS"], header=True)
    add_table_row(table, ["Cau truc du lieu", "Hang doi (FIFO)", "Ngan xep (LIFO)"])
    add_table_row(table, ["Do chinh xac", "Luon tim duong it canh nhat", "Khong dam bao it canh nhat"])
    add_table_row(table, ["Do phuc tap", "O(V + E)", "O(V + E)"])
    add_table_row(table, ["Bo nho", "Ton nhieu hon", "It hon, phu hop do thi sau"])

    doc.add_paragraph()

    # ===== CHUONG IV: BIPARTITE & COLORING =====
    doc.add_heading("4. Chuong IV: Kiem tra hai phia & To mau", level=1)

    doc.add_heading("4.1 Kiem tra do thi hai phia", level=2)
    doc.add_paragraph("Do thi KHONG la do thi hai phia (chua chu trinh do dai le).")

    doc.add_heading("4.2 To mau (Welsh-Powell)", level=2)
    doc.add_paragraph("So mau can dung: 2")
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Dinh", "Bac", "Mau"], header=True)
    coloring_data = [
        ("A", 3, 0), ("B", 2, 1), ("C", 3, 0), ("D", 2, 1),
        ("E", 2, 1), ("F", 3, 0), ("G", 2, 0), ("H", 2, 0),
        ("I", 1, 0), ("J", 0, 0),
    ]
    for node, deg, color in coloring_data:
        add_table_row(table, [node, str(deg), str(color)])

    doc.add_paragraph()

    # Code
    doc.add_heading("4.3 Code - Kiem tra hai phia", level=2)
    code_bipartite = '''def check_bipartite(graph):
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
    return True, coloring'''
    doc.add_paragraph(code_bipartite, style='Normal')

    doc.add_heading("4.4 Code - To mau Welsh-Powell", level=2)
    code_coloring = '''def graph_coloring(graph):
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
    doc.add_paragraph(code_coloring, style='Normal')

    doc.add_paragraph()

    # ===== CHUONG V: SHORTEST PATH =====
    doc.add_heading("5. Chuong V: Duong di ngan nhat", level=1)

    doc.add_heading("5.1 Dijkstra (tu A)", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Dinh", "Khoang cach", "Duong di"], header=True)
    dijkstra_data = [
        ("A", "0", "A"),
        ("B", "4", "A -> B"),
        ("C", "2", "A -> C"),
        ("D", "4", "A -> C -> D"),
        ("E", "5", "A -> C -> E"),
        ("F", "6", "A -> C -> F"),
        ("G", "8", "A -> C -> F -> G"),
        ("H", "10", "A -> C -> E -> H"),
        ("I", "9", "A -> C -> F -> G -> I"),
        ("J", "7", "A -> C -> F -> J"),
    ]
    for node, dist, path in dijkstra_data:
        add_table_row(table, [node, dist, path])

    doc.add_paragraph()
    doc.add_paragraph("Bellman-Ford cho ket qua giong Dijkstra (khong co trong so am).")

    doc.add_heading("5.2 So sanh Dijkstra vs Bellman-Ford", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Tieu chi", "Dijkstra", "Bellman-Ford"], header=True)
    add_table_row(table, ["Trong so am", "Khong xu ly duoc", "Xu ly duoc"])
    add_table_row(table, ["Phat hien chu trinh am", "Khong", "Co"])
    add_table_row(table, ["Do phuc tap", "O((V+E) log V)", "O(V*E)"])

    doc.add_paragraph()

    # Code
    doc.add_heading("5.3 Code - Dijkstra", level=2)
    code_dijkstra = '''def dijkstra(graph, source):
    INF = 999999999
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
    return dist, parent'''
    doc.add_paragraph(code_dijkstra, style='Normal')

    doc.add_heading("5.4 Code - Bellman-Ford", level=2)
    code_bf = '''def bellman_ford(graph, source):
    INF = 999999999
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
    return dist, parent, has_neg'''
    doc.add_paragraph(code_bf, style='Normal')

    doc.add_paragraph()

    # ===== CHUONG VII.1-7.2: EULER =====
    doc.add_heading("6. Chuong VII.1-7.2: Chu trinh / Duong di Euler", level=1)

    doc.add_heading("6.1 Kiem tra dieu kien Euler", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Dinh", "Bac", "Chan/Le"], header=True)
    euler_data = [
        ("A", 3, "LE"), ("B", 2, "Chan"), ("C", 3, "LE"), ("D", 2, "Chan"),
        ("E", 2, "Chan"), ("F", 3, "LE"), ("G", 2, "Chan"), ("H", 2, "Chan"),
        ("I", 1, "LE"), ("J", 0, "Chan"),
    ]
    for node, deg, chan_le in euler_data:
        add_table_row(table, [node, str(deg), chan_le])

    doc.add_paragraph()
    doc.add_paragraph("=> KHONG co duong/chu trinh Euler (4 dinh bac le: A, C, F, I)")

    doc.add_heading("6.2 Code - Hierholzer", level=2)
    code_hier = '''def hierholzer(graph, start=None):
    odd_nodes = [n for n in graph.nodes if graph.get_degree(n) % 2 == 1]
    if len(odd_nodes) == 0:
        start = start or graph.nodes[0]
    elif len(odd_nodes) == 2:
        start = start if start in odd_nodes else odd_nodes[0]
    else:
        return None  # Khong co Euler

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
    return circuit'''
    doc.add_paragraph(code_hier, style='Normal')

    doc.add_paragraph()

    # ===== CHUONG VII.3-7.4: MST =====
    doc.add_heading("7. Chuong VII.3-7.4: Cay khung nho nhat (MST)", level=1)
    doc.add_paragraph("Ap dung cho do thi vo huong (bo huong cac canh).")

    doc.add_heading("7.1 Ket qua Prim", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Tu", "Den", "Trong so"], header=True)
    prim_data = [
        ("A", "C", 2), ("C", "B", 1), ("C", "D", 2), ("C", "E", 3),
        ("E", "F", 3), ("F", "J", 1), ("F", "G", 2), ("G", "I", 1),
        ("J", "H", 2),
    ]
    for u, v, w in prim_data:
        add_table_row(table, [u, v, str(w)])
    add_table_row(table, ["", "TONG", "17"], bold=True)

    doc.add_paragraph()

    doc.add_heading("7.2 Ket qua Kruskal", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Tu", "Den", "Trong so"], header=True)
    kruskal_data = [
        ("B", "C", 1), ("F", "J", 1), ("G", "I", 1),
        ("A", "C", 2), ("C", "D", 2), ("F", "G", 2), ("H", "J", 2),
        ("C", "E", 3), ("E", "F", 3),
    ]
    for u, v, w in kruskal_data:
        add_table_row(table, [u, v, str(w)])
    add_table_row(table, ["", "TONG", "17"], bold=True)

    doc.add_paragraph()
    doc.add_paragraph("Kruskal = Prim = 17 (khop).")

    doc.add_heading("7.3 So sanh Kruskal vs Prim", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Thuat toan", "Giai quyet", "Do phuc tap"], header=True)
    add_table_row(table, ["Kruskal", "MST - tham lam theo canh", "O(E log E)"])
    add_table_row(table, ["Prim", "MST - tham lam theo dinh", "O(E log V)"])

    doc.add_paragraph()

    # Code
    doc.add_heading("7.4 Code - Union-Find", level=2)
    code_uf = '''class UnionFind:
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
        return True'''
    doc.add_paragraph(code_uf, style='Normal')

    doc.add_heading("7.5 Code - Prim", level=2)
    code_prim = '''def prim(graph, start=None):
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
    return mst_edges, total'''
    doc.add_paragraph(code_prim, style='Normal')

    doc.add_heading("7.6 Code - Kruskal", level=2)
    code_kruskal = '''def kruskal(graph):
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
    doc.add_paragraph(code_kruskal, style='Normal')

    doc.add_paragraph()

    # ===== CHUONG VII.5: MAX FLOW =====
    doc.add_heading("8. Chuong VII.5: Luong toi da (Ford-Fulkerson)", level=1)
    doc.add_paragraph("Nguon: A, Dich: J")

    doc.add_heading("8.1 Cac buocFord-Fulkerson", level=2)
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    add_table_row(table, ["Buoc", "Duong dan (luong)"], header=True)
    ff_steps = [
        ("1", "A -> C -> F -> J (+1)"),
        ("2", "A -> D -> G -> J (+4)"),
        ("3", "A -> B -> E -> H -> J (+2)"),
        ("4", "A -> C -> F -> I -> J (+1)"),
        ("5", "A -> D -> G -> I -> J (+1)"),
        ("6", "A -> B -> C -> F -> I -> J (+1)"),
        ("7", "A -> B -> E -> F -> I -> J (+1)"),
    ]
    for step, path in ff_steps:
        add_table_row(table, [step, path])
    add_table_row(table, ["", "LUONG TOI DA = 11"], bold=True)

    doc.add_paragraph()

    doc.add_heading("8.2 Luong tren moi canh", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Canh", "Luong", "Dung luong"], header=True)
    flow_data = [
        ("A -> B", "4", "4"), ("A -> C", "2", "2"), ("A -> D", "5", "7"),
        ("B -> C", "1", "1"), ("B -> E", "3", "5"),
        ("C -> F", "3", "4"),
        ("D -> G", "5", "6"),
        ("E -> F", "1", "3"), ("E -> H", "2", "5"),
        ("F -> I", "3", "6"), ("F -> J", "1", "1"),
        ("G -> I", "1", "1"), ("G -> J", "4", "4"),
        ("H -> J", "2", "2"),
        ("I -> J", "4", "4"),
    ]
    for canh, luong, dung_luong in flow_data:
        add_table_row(table, [canh, luong, dung_luong])

    doc.add_paragraph()

    # Code
    doc.add_heading("8.3 Code - Ford-Fulkerson", level=2)
    code_ff = '''def ford_fulkerson(graph, source, sink):
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
    doc.add_paragraph(code_ff, style='Normal')

    doc.add_paragraph()

    # ===== TONG QUAT =====
    doc.add_heading("9. Tong quat thuat toan", level=1)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    add_table_row(table, ["Thuat toan", "Giai quyet", "Do phuc tap"], header=True)
    algo_summary = [
        ("BFS", "Duyet theo lop, duong it canh nhat", "O(V+E)"),
        ("DFS", "Duyet theo chieu sau, phat hien chu trinh", "O(V+E)"),
        ("Kiem tra hai phia", "To 2 mau bang BFS", "O(V+E)"),
        ("To mau Welsh-Powell", "To mau tham lam, xap xi sac so", "O(V^2)"),
        ("Dijkstra", "Duong ngan nhat, trong so >= 0", "O((V+E) log V)"),
        ("Bellman-Ford", "Duong ngan nhat, trong so am", "O(V*E)"),
        ("Kruskal", "MST - tham lam theo canh", "O(E log E)"),
        ("Prim", "MST - tham lam theo dinh", "O(E log V)"),
        ("Hierholzer", "Chu trinh / duong di Euler", "O(E)"),
        ("Ford-Fulkerson", "Luong toi da", "O(E * max_flow)"),
    ]
    for ten, giai, do_phuc_tap in algo_summary:
        add_table_row(table, [ten, giai, do_phuc_tap])

    doc.add_paragraph()

    # ===== CHON THUAT TOAN =====
    doc.add_heading("10. Huong dan chon thuat toan", level=1)
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    add_table_row(table, ["Nhu cau bai toan", "Thuat toan nen dung"], header=True)
    guide = [
        ("Chi can biet 'den duoc hay khong / it buoc nhat'", "BFS"),
        ("Duyet het do thi, phat hien chu trinh, duong di bat ky", "DFS"),
        ("Duong di re nhat, trong so khong am", "Dijkstra"),
        ("Duong di re nhat, co the co trong so am", "Bellman-Ford"),
        ("Noi moi dinh voi chi phi thap nhat", "Kruskal / Prim"),
        ("Phai di qua tung canh dung 1 lan", "Kiem tra Euler -> Hierholzer"),
        ("Chay luong toi da trong mang luoi", "Ford-Fulkerson"),
    ]
    for nhu_cau, thuat_toan in guide:
        add_table_row(table, [nhu_cau, thuat_toan])

    # Save
    output_path = "/home/hungvo/Downloads/BangKetQua_Dothi_10Dinh.docx"
    doc.save(output_path)
    print(f"Da luu: {output_path}")


if __name__ == "__main__":
    create_docx()
