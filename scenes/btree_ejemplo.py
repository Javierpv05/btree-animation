# Escena 7: ejemplo con inserción, eliminación y búsqueda.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree import BTree
from utils.btree_layout import (
    titulo, caption, tree_to_vgroup, switch_caption,
)


DEGREE        = 3
KEYS_INSERT   = [10, 20, 5, 6, 12, 30, 7, 17]
KEYS_DELETE   = [6, 30]
KEY_SEARCH    = 7


class BTreeEjemplo(Scene):
    def construct(self):
        t = Text(
            f"Ejemplo: B-Tree de grado m = {DEGREE}",
            font_size=34,
            color=GREEN,
        ).move_to([0, 3.4, 0])

        self.play(Write(t), run_time=1)
        self.wait(0.5)

        tree = BTree(degree=DEGREE)
        cur = None
        cap = None

        keys_text = self.keys_label(KEYS_INSERT, "Insertar:", color=YELLOW)
        self.play(FadeIn(keys_text, shift=RIGHT), run_time=0.6)
        self.wait(0.8)

        for k in KEYS_INSERT:
            cur, cap = self.animate_op(tree, k, "insert", cur, cap)

        self.play(FadeOut(keys_text), run_time=0.5)
        self.wait(0.6)

        del_text = self.keys_label(KEYS_DELETE, "Eliminar:", color=RED)
        self.play(FadeIn(del_text, shift=RIGHT), run_time=0.6)
        self.wait(0.8)

        for k in KEYS_DELETE:
            cur, cap = self.animate_op(tree, k, "delete", cur, cap)

        self.play(FadeOut(del_text), run_time=0.5)
        self.wait(0.6)

        search_text = self.keys_label([KEY_SEARCH], "Buscar:", color=BLUE)
        self.play(FadeIn(search_text, shift=RIGHT), run_time=0.8)
        self.wait(1.0)

        cur, cap = self.animate_op(tree, KEY_SEARCH, "search", cur, cap)

        self.play(FadeOut(search_text), run_time=0.5)

        cierre = caption("Insertar, eliminar y buscar en O(log n).")
        self.play(*switch_caption(cap, cierre), run_time=0.8)
        self.wait(2.5)

        self.play(FadeOut(VGroup(t, cur, cierre)))

    def keys_label(self, keys, prefix, color, y_offset=0.9):
        texto = Text(
            f"{prefix}  " + ", ".join(str(k) for k in keys),
            font_size=22,
            color=color,
        )
        return texto.to_corner(UL, buff=0.5).shift(DOWN * y_offset)

    def animate_op(self, tree, key, op, cur, cap):
        if op == "insert":
            steps = tree.insert_with_steps(key)
        elif op == "delete":
            steps = tree.delete_with_steps(key)
        else:
            steps = tree.search_with_steps(key)

        if op == "delete":
            rt = 0.9
            pause = 0.9
        elif op == "search":
            rt = 0.6
            pause = 0.4
        else:
            rt = 0.7
            pause = 0.45

        for step in steps:
            new_mob = tree_to_vgroup(
                step.tree,
                highlight_path=step.highlight_path,
            )
            new_cap = caption(step.caption)

            pausa_extra = 0.0
            if any(p in step.caption.lower()
                   for p in ("split", "merge", "predecesor", "sucesor")):
                pausa_extra = 0.7

            if cur is None:
                self.play(
                    FadeIn(new_mob),
                    FadeIn(new_cap, shift=UP),
                    run_time=rt,
                )
            else:
                # 1) Desvanecer el árbol viejo y su caption
                self.play(
                    FadeOut(cur),
                    FadeOut(cap),
                    run_time=rt * 0.35,
                )
                # 2) Eliminar COMPLETAMENTE del scene graph
                self.remove(cur, cap)
                # 3) Aparición limpia del nuevo árbol y caption
                self.play(
                    FadeIn(new_mob),
                    FadeIn(new_cap, shift=UP),
                    run_time=rt * 0.65,
                )

            self.wait(pause + pausa_extra)
            cur, cap = new_mob, new_cap

        return cur, cap