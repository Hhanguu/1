"""
main.py - Menu chinh cua ung dung do thi
Chay: python3 main.py (hoac python main.py tren Windows)
"""



def show_menu():
    """Hien thi menu chinh"""
    print("\n" + "=" * 60)
    print("       UNG DUNG DO THI - TAT CA CAC THUAT TOAN")
    print("=" * 60)
    print("  Phan co ban:")
    print("    1. Nhap do thi, Ve & Luu hinh, Bieu dien (Q1 & Q2)")
    print("    2. Duyet BFS & DFS (Q3)")
    print("    3. Kiem tra do thi hai phia (Q4)")
    print("    4. Duong di ngan nhat - Dijkstra & Bellman-Ford (Q5)")
    print("")
    print("  Phan nang cao:")
    print("    5. Cu trinh Euler - Fleury & Hierholzer (Q7.1 & Q7.2)")
    print("    6. Cay khung nho nhat - Prim & Kruskal (Q7.3 & Q7.4)")
    print("    7. Luong toi da - Ford-Fulkerson (Q7.5)")
    print("    8. Bai toan thuc te - Mang luoi nuoc (Q8)")
    print("")
    print("    0. Thoat")
    print("=" * 60)


def main():
    """Ham main - menu chon module"""
    while True:
        show_menu()
        choice = input("Chon module (0-8): ").strip()

        if choice == "0":
            print("Tam biet!")
            break
        elif choice == "1":
            from q1q2_repr import run_module1
            run_module1()
        elif choice == "2":
            from q3_traversal import run_module2
            run_module2()
        elif choice == "3":
            from q4_bipartite import run_module3
            run_module3()
        elif choice == "4":
            from q5_shortest import run_module4
            run_module4()
        elif choice == "5":
            from q71q72_eulerian import run_module5
            run_module5()
        elif choice == "6":
            from q73q74_mst import run_module6
            run_module6()
        elif choice == "7":
            from q75_maxflow import run_module7
            run_module7()
        elif choice == "8":
            from q8_realworld import run_module8
            run_module8()
        else:
            print("Lua chon khong hop le!")

        input("\nNhan Enter de quay lai menu...")


if __name__ == "__main__":
    main()
