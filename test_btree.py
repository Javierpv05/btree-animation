"""Test rápido del algoritmo B-Tree. Ejecuta: python test_btree.py"""
from utils.btree import BTree, validar


def print_tree(node, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "
    print(prefix + connector + str(node.keys))
    new_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(node.children):
        print_tree(child, new_prefix, i == len(node.children) - 1)


def test_insert_grado3():
    print("=== Inserciones con grado 3 ===")
    tree = BTree(degree=3)
    for k in [10, 20, 30, 40, 50, 60, 70, 80]:
        tree.insert_silent(k)
        ok, msg = validar(tree.root, 3)
        assert ok, f"Tras insertar {k}: {msg}"
    print_tree(tree.root)
    print("OK: 8 inserciones, árbol siempre válido\n")


def test_delete_grado4():
    print("=== Eliminaciones con grado 4 ===")
    tree = BTree(degree=4)
    for k in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
        tree.insert_silent(k)
    ok, msg = validar(tree.root, 4)
    assert ok, f"Árbol inicial: {msg}"
    print_tree(tree.root)

    for k in [30, 20, 70]:
        tree.delete_with_steps(k)
        ok, msg = validar(tree.root, 4)
        assert ok, f"Tras eliminar {k}: {msg}"
        print(f"\nTras eliminar {k}:")
        print_tree(tree.root)

    print("\nOK: eliminaciones preservan invariantes\n")


def test_delete_grado3_solo_hojas():
    print("=== Eliminaciones con grado 3 (solo hojas) ===")
    tree = BTree(degree=3)
    for k in [10, 20, 30, 40]:
        tree.insert_silent(k)

    tree.delete_with_steps(10)   # hoja con préstamo o merge
    ok, msg = validar(tree.root, 3)
    assert ok, f"Tras eliminar 10: {msg}"
    print_tree(tree.root)
    print("OK\n")


if __name__ == "__main__":
    test_insert_grado3()
    test_delete_grado4()
    test_delete_grado3_solo_hojas()
    print("✅ Todos los tests pasaron.")