# Escena 4: qué es un B-Tree y comparación con el BST.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import FS_TEXTO, FS_ETIQUETA, make_node, titulo, caption


class BTreeIntro(Scene):
    def construct(self):
        t = titulo("El B-Tree")
        self.play(Write(t), run_time=0.8)

        defi = Text(
            "Árbol multicamino: cada nodo guarda\nvarias claves y tiene varios hijos.",
            font_size=FS_TEXTO, line_spacing=1.3,
        ).move_to([0, 2, 0])
        self.play(FadeIn(defi, shift=UP), run_time=0.8)

        nodo = make_node([20, 40, 60], color=YELLOW).move_to([0, 0.3, 0])
        self.play(FadeIn(nodo, shift=DOWN), run_time=0.8)

        rangos = ["< 20", "20–40", "40–60", "> 60"]
        xs = [
            nodo[0][0].get_left()[0] - 0.7,
            (nodo[0][0].get_right()[0] + nodo[0][1].get_left()[0]) / 2,
            (nodo[0][1].get_right()[0] + nodo[0][2].get_left()[0]) / 2,
            nodo[0][2].get_right()[0] + 0.7,
        ]
        etiq = VGroup(*[
            Text(txt, font_size=FS_ETIQUETA, color=BLUE).move_to([x, -0.7, 0])
            for txt, x in zip(rangos, xs)
        ])
        self.play(LaggedStart(*[FadeIn(e, shift=UP) for e in etiq], lag_ratio=0.15),
                  run_time=1)

        msg = caption("3 claves → 4 hijos. Cada hijo cubre un rango.")
        self.play(Write(msg), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(VGroup(t, defi, nodo, etiq, msg)))

        ct = titulo("BST  vs  B-Tree")
        self.play(Write(ct), run_time=0.8)

        bst_lbl = Text("BST", font_size=26, color=BLUE).move_to([-4, 1.6, 0])
        bst_nodos = VGroup()
        for i, (dx, dy) in enumerate([(0, 1), (-1, 0), (1, 0)]):
            c = Circle(radius=0.25, color=BLUE, stroke_width=2)
            n = Text(str([30, 15, 45][i]), font_size=16).move_to(c)
            bst_nodos.add(VGroup(c, n).move_to([-4 + dx, dy, 0]))
        bst_lin = VGroup(
            Line(bst_nodos[0].get_bottom(), bst_nodos[1].get_top(), color=BLUE, stroke_width=2),
            Line(bst_nodos[0].get_bottom(), bst_nodos[2].get_top(), color=BLUE, stroke_width=2),
        )

        bt_lbl = Text("B-Tree", font_size=26, color=GREEN).move_to([4, 1.6, 0])
        bt_nodo = make_node([20, 50], color=GREEN).move_to([4, 1, 0])
        bt_hijos = VGroup()
        for i, v in enumerate([10, 30, 70]):
            c = Circle(radius=0.25, color=GREEN, stroke_width=2)
            n = Text(str(v), font_size=16).move_to(c)
            bt_hijos.add(VGroup(c, n).move_to([4 - 1 + i * 1, -0.3, 0]))
        bt_lin = VGroup(*[
            Line(bt_nodo.get_bottom(), h.get_top(), color=GREEN, stroke_width=2)
            for h in bt_hijos
        ])

        self.play(
            FadeIn(bst_lbl), FadeIn(bt_lbl),
            LaggedStart(*[FadeIn(n) for n in bst_nodos], lag_ratio=0.1),
            LaggedStart(*[Create(l) for l in bst_lin], lag_ratio=0.1),
            FadeIn(bt_nodo),
            LaggedStart(*[FadeIn(n) for n in bt_hijos], lag_ratio=0.1),
            LaggedStart(*[Create(l) for l in bt_lin], lag_ratio=0.1),
            run_time=1.5,
        )

        eb = Text("1 clave · 2 hijos", font_size=18, color=BLUE).move_to([-4, -1.5, 0])
        et = Text("muchas claves · muchos hijos", font_size=18, color=GREEN).move_to([4, -1.5, 0])
        self.play(FadeIn(eb), FadeIn(et), run_time=0.6)

        cierre = caption("El B-Tree generaliza el BST a múltiples ramas.")
        self.play(Write(cierre), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(VGroup(ct, bst_lbl, bst_nodos, bst_lin,
                                  bt_lbl, bt_nodo, bt_hijos, bt_lin, eb, et, cierre)))