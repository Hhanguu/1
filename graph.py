"""
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
        """
        Khoi tao do thi
        nodes: danh sach dinh, vi du [0,1,2,...] hoac ['A','B',...]
        edges: danh sach canh [(u,v,w), ...] hoac [(u,v), ...]
        is_directed: True neu do thi co huong
        weighted: True neu do thi co trong so
        """
        self.nodes = list(nodes) if nodes else []
        self.is_directed = is_directed
        self.weighted = weighted
        self.adj = {}  # danh sach ke: {dinh: [(lang gieng, trong so), ...]}

        # Khoi tao danh sach ke rong cho moi dinh
        for node in self.nodes:
            self.adj[node] = []

        # Them cac canh
        if edges:
            for edge in edges:
                if len(edge) == 3:
                    u, v, w = edge
                else:
                    u, v = edge
                    w = 1
                self.add_edge(u, v, w)

    def add_edge(self, u, v, w=1):
        """Them canh tu u den v voi trong so w"""
        self.adj[u].append((v, w))
        if not self.is_directed:
            self.adj[v].append((u, w))

    def remove_edge(self, u, v, w=None):
        """Xoa mot canh tu u den v. Neu w=None, xoa canh dau tien tim thay"""
        removed = False
        new_adj_u = []
        for nb, weight in self.adj[u]:
            if nb == v and not removed and (w is None or weight == w):
                removed = True
                continue
            new_adj_u.append((nb, weight))
        self.adj[u] = new_adj_u

        if not self.is_directed:
            removed = False
            new_adj_v = []
            for nb, weight in self.adj[v]:
                if nb == u and not removed and (w is None or weight == w):
                    removed = True
                    continue
                new_adj_v.append((nb, weight))
            self.adj[v] = new_adj_v

    def get_neighbors(self, node):
        """Lay danh sach lang gieng cua dinh (dinh, trong so)"""
        return list(self.adj.get(node, []))

    def get_degree(self, node):
        """Lay bac cua dinh"""
        return len(self.adj.get(node, []))

    def get_all_edges(self):
        """Lay tat ca canh duoi dang (u, v, w)"""
        edges = []
        seen = set()
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

    # ========== CAC PHEP BIEU DIEN ==========

    def get_adjacency_matrix(self):
        """Tra ve ma tran ke"""
        n = len(self.nodes)
        idx = {}
        for i, node in enumerate(self.nodes):
            idx[node] = i

        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(0)
            matrix.append(row)

        for u in self.nodes:
            for v, w in self.adj[u]:
                matrix[idx[u]][idx[v]] = w

        return matrix, self.nodes

    def get_adjacency_list(self):
        """Tra ve danh sach ke"""
        result = {}
        for node in self.nodes:
            result[node] = list(self.adj[node])
        return result

    def get_edge_list(self):
        """Tra ve danh sach canh"""
        return self.get_all_edges()

    def display_representations(self):
        """Hien thi tat ca cac phep bieu dien"""
        print("\n" + "=" * 60)
        print("       CAC PHEP BIEU DIEN DO THI")
        print("=" * 60)

        # 1. Ma tran ke
        matrix, nodes = self.get_adjacency_matrix()
        print("\n1. MA TRAN KE (Adjacency Matrix):")
        print("   ", end="")
        for node in nodes:
            print(f"{node:>5}", end="")
        print()
        print("   " + "-" * (5 * len(nodes) + 2))
        for i, node in enumerate(nodes):
            print(f"  {node}|", end="")
            for j in range(len(nodes)):
                print(f"{matrix[i][j]:>5}", end="")
            print()

        # 2. Danh sach ke
        adj_list = self.get_adjacency_list()
        print("\n2. DANH SACH KE (Adjacency List):")
        for node in self.nodes:
            neighbors = adj_list[node]
            items = []
            for nb, w in neighbors:
                if self.weighted:
                    items.append(f"{nb}({w})")
                else:
                    items.append(f"{nb}")
            print(f"   {node}: {', '.join(items)}")

        # 3. Danh sach canh
        edge_list = self.get_edge_list()
        print("\n3. DANH SACH CANH (Edge List):")
        items = []
        for u, v, w in edge_list:
            if self.weighted:
                items.append(f"({u},{v},{w})")
            else:
                items.append(f"({u},{v})")
        print(f"   [{', '.join(items)}]")
        print("=" * 60)

    def draw_graph(self, filename="graph.png", title="Do Thi", node_colors=None, highlight_edges=None):
        """
        Ve do thi va luu thanh hinh anh.
        node_colors: dict {node: (r,g,b)} mau sac tu cho, 0.0-1.0
        highlight_edges: list cac canh [(u,v), ...] de lam noi bat
        """
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print("  Can cai matplotlib: pip install matplotlib")
            return None

        try:
            import networkx as nx
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
        except ImportError:
            n = len(self.nodes)
            pos = {}
            for i, node in enumerate(self.nodes):
                angle = 2 * math.pi * i / n
                pos[node] = (math.cos(angle), math.sin(angle))

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
                    ax.annotate(
                        "", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="-|>" if self.is_directed else "-",
                                        color=color, lw=lw, shrinkA=12, shrinkB=12),
                    )
                    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                    if self.weighted:
                        ax.text(mx, my, str(w), fontsize=8, ha="center", va="center",
                                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.8))

        for node in self.nodes:
            x, y = pos[node]
            if node_colors and node in node_colors:
                c = node_colors[node]
                if isinstance(c, str):
                    color = c
                else:
                    color = (c[0], c[1], c[2])
            else:
                color = "lightblue"
            circle = plt.Circle((x, y), 0.08, color=color, ec="black", lw=1.5, zorder=5)
            ax.add_patch(circle)
            ax.text(x, y, str(node), ha="center", va="center", fontsize=10, fontweight="bold", zorder=6)

        margin = 0.3
        ax.set_xlim(-1 - margin, 1 + margin)
        ax.set_ylim(-1 - margin, 1 + margin)

        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Da luu hinh: {filename}")
        return filename

    def copy(self):
        """Tao ban sao cua do thi"""
        edges = self.get_all_edges()
        return Graph(
            nodes=list(self.nodes),
            edges=list(edges),
            is_directed=self.is_directed,
            weighted=self.weighted,
        )
