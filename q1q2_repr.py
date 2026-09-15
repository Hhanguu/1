"""
module1_repr.py - Q1 & Q2: Nhap do thi, ve, luu hinh, hien thi bieu dien
Khong su dung bat ky thu vien nao
"""

from graph import Graph
from examples import create_sample_graph, create_20_undirected, create_20_directed



def input_graph_manual():
    print("\n--- NHAP DO THI TU BAN PHIM ---")
    while True:
        try:
            n = int(input("Nhap so dinh: "))
            if n <= 0:
                print("So dinh phai > 0")
                continue
            break
        except Exception:
            print("Nhap so nguyen!")

    print("Nhap ten " + str(n) + " dinh (nhan Enter de dung 0,1,2,...):")
    nodes = []
    for i in range(n):
        name = input("  Dinh " + str(i + 1) + ": ").strip()
        if name == "":
            name = i
        else:
            try:
                name = int(name)
            except Exception:
                pass
        nodes.append(name)

    directed = input("Do thi co huong? (y/n, mac dinh n): ").strip().lower()
    is_directed = directed == "y"
    weighted = input("Do thi co trong so? (y/n, mac dinh y): ").strip().lower()
    is_weighted = weighted != "n"

    print("\nNhap cac canh (dinh_dau dinh_cuoi [trong so]):")
    print("  Vi du: 0 1 5")
    print("  Nhap 'xong' de ket thuc")
    edges = []
    while True:
        line = input("  Canh: ").strip()
        if line.lower() == "xong" or line == "":
            break
        parts = line.split()
        if len(parts) < 2:
            print("  Can it nhat 2 dinh!")
            continue
        try:
            u = parts[0]
            try:
                u = int(u)
            except Exception:
                pass
            v = parts[1]
            try:
                v = int(v)
            except Exception:
                pass
            w = 1
            if len(parts) >= 3 and is_weighted:
                w = float(parts[2])
                if w == int(w):
                    w = int(w)
            edges.append((u, v, w))
        except Exception as e:
            print("  Loi: " + str(e))

    return Graph(nodes=nodes, edges=edges, is_directed=is_directed, weighted=is_weighted)


def run_module1():
    print("\n" + "=" * 60)
    print("  MODULE 1: NHAP DO THI, VE DO THI & BIEU DIEN")
    print("  (Cau 1 & 2)")
    print("=" * 60)
    print("\nChon loai do thi:")
    print("  1. Nhap tu ban phim")
    print("  2. Do thi mau A-J (10 dinh)")
    print("  3. Do thi 20 dinh VO HUONG")
    print("  4. Do thi 20 dinh CO HUONG")

    choice = input("Chon (1-4): ").strip()
    if choice == "1":
        graph = input_graph_manual()
    elif choice == "2":
        graph = create_sample_graph()
        print("Da tai do thi mau A-J (10 dinh)")
    elif choice == "3":
        graph = create_20_undirected()
        print("Da tai do thi 20 dinh VO HUONG")
    elif choice == "4":
        graph = create_20_directed()
        print("Da tai do thi 20 dinh CO HUONG")
    else:
        print("Lua chon khong hop le, su dung do thi mau")
        graph = create_sample_graph()

    print("\nSo dinh: " + str(len(graph.nodes)))
    print("So canh: " + str(len(graph.get_all_edges())))
    loai = "Co huong" if graph.is_directed else "Vo huong"
    print("Loai: " + loai)

    print("\n--- VE DO THI ---")

    graph.draw_graph(filename="graph_output.png", title="Do Thi (Q1)")

    graph.display_representations()
    print("\n--- Hoan thanh Module 1 ---")


if __name__ == "__main__":
    run_module1()
