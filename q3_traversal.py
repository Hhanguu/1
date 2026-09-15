"""
module2_traversal.py - Q3: BFS & DFS
Khong su dung bat ky thu vien nao
"""

from graph import Graph
from examples import create_sample_graph, create_20_undirected



def bfs(graph, start):
    visited = {}
    queue = [start]
    order = []
    visited[start] = 1
    while len(queue) > 0:
        node = queue.pop(0)
        order.append(node)
        neighbors = []
        for nb, w in graph.get_neighbors(node):
            if nb not in visited:
                neighbors.append(nb)
        neighbors.sort()
        for nb in neighbors:
            visited[nb] = 1
            queue.append(nb)
    return order


def dfs(graph, start):
    visited = {}
    stack = [start]
    order = []
    while len(stack) > 0:
        node = stack.pop()
        if node in visited:
            continue
        visited[node] = 1
        order.append(node)
        neighbors = []
        for nb, w in graph.get_neighbors(node):
            if nb not in visited:
                neighbors.append(nb)
        neighbors.sort(reverse=True)
        for nb in neighbors:
            stack.append(nb)
    return order


def bfs_shortest_path(graph, start, end):
    if start == end:
        return [start]
    visited = {}
    queue = [start]
    parent = {}
    visited[start] = 1
    parent[start] = None
    while len(queue) > 0:
        node = queue.pop(0)
        for nb, w in graph.get_neighbors(node):
            if nb not in visited:
                visited[nb] = 1
                parent[nb] = node
                queue.append(nb)
                if nb == end:
                    path = []
                    current = end
                    while current is not None:
                        path.append(current)
                        current = parent[current]
                    path.reverse()
                    return path
    return None


def run_module2():
    print("\n" + "=" * 60)
    print("  MODULE 2: DUYET DO THI - BFS & DFS")
    print("  (Cau 3)")
    print("=" * 60)

    print("\nChon do thi:")
    print("  1. Do thi mau A-J (10 dinh)")
    print("  2. Do thi 20 dinh VO HUONG")
    print("  3. Nhap tu ban phim")
    choice = input("Chon (1-3): ").strip()

    if choice == "1":
        graph = create_sample_graph()
        hand_results = {"bfs_0": [0, 1, 2, 3, 4, 5], "dfs_0": [0, 1, 3, 2, 4, 5]}
    elif choice == "2":
        graph = create_20_undirected()
        hand_results = None
    else:
        from q1q2_repr import input_graph_manual
        graph = input_graph_manual()
        hand_results = None

    print("\nDo thi: " + str(len(graph.nodes)) + " dinh, " + str(len(graph.get_all_edges())) + " canh")
    print("Loai: " + ("Co huong" if graph.is_directed else "Vo huong"))

    while True:
        try:
            start = input("\nNhap dinh bat dau " + str(graph.nodes) + ": ").strip()
            try:
                start = int(start)
            except Exception:
                pass
            if start in graph.nodes:
                break
            print("Dinh khong ton tai!")
        except Exception:
            print("Nhap sai!")

    # BFS
    print("\n" + "-" * 40)
    print("  BFS - DUYET THEO CHIEU RONG")
    print("-" * 40)
    bfs_result = bfs(graph, start)
    print("\nKet qua BFS tu dinh " + str(start) + ":")
    print("  Thu tu duyet: " + str(bfs_result))

    if hand_results and start == 0:
        expected = hand_results["bfs_0"]
        print("  Ket qua thu cong: " + str(expected))
        if bfs_result == expected:
            print("  => KHOP voi ket qua thu cong!")
        else:
            print("  => KHONG khop!")

    nc = {}
    for i in range(len(bfs_result)):
        r = 0.3 + 0.7 * i / max(1, len(bfs_result) - 1)
        if r > 1.0:
            r = 1.0
        g = 0.8 - 0.8 * i / max(1, len(bfs_result) - 1)
        if g < 0.0:
            g = 0.0
        nc[bfs_result[i]] = (r, g, 0.2)

    # DFS
    print("\n" + "-" * 40)
    print("  DFS - DUYET THEO SAU")
    print("-" * 40)
    dfs_result = dfs(graph, start)
    print("\nKet qua DFS tu dinh " + str(start) + ":")
    print("  Thu tu duyet: " + str(dfs_result))

    if hand_results and start == 0:
        expected = hand_results["dfs_0"]
        print("  Ket qua thu cong: " + str(expected))
        if dfs_result == expected:
            print("  => KHOP voi ket qua thu cong!")
        else:
            print("  => KHONG khop!")

    nc2 = {}
    for i in range(len(dfs_result)):
        r = 0.3 + 0.7 * i / max(1, len(dfs_result) - 1)
        if r > 1.0:
            r = 1.0
        b = 0.8 - 0.8 * i / max(1, len(dfs_result) - 1)
        if b < 0.0:
            b = 0.0
        nc2[dfs_result[i]] = (r, 0.2, b)

    # In do thi terminal
    nc_term = {}
    for i in range(len(bfs_result)):
        nc_term[bfs_result[i]] = "G"

    print("\n--- Hoan thanh Module 2 ---")

    graph.draw_graph(
        filename="graph_bfs.png",
        title="BFS tu dinh " + str(start),
        node_colors={n: "lightgreen" for n in bfs_result},
    )
    graph.draw_graph(
        filename="graph_dfs.png",
        title="DFS tu dinh " + str(start),
        node_colors={n: "lightyellow" for n in dfs_result},
    )
    print("  Da luu: graph_bfs.png, graph_dfs.png")


if __name__ == "__main__":
    run_module2()
