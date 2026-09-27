# Escena 4: qué es un B-Tree, ventaja y comparación con el BST.
# Las flechas del B-Tree salen del intermedio entre dos claves.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import (
    FS_TEXTO, FS_ETIQUETA, KEY_W, KEY_H,
    make_node, titulo, caption, switch_caption,
)


def _start_points(x_center, y_center, n_keys):
    """Puntos de salida de las aristas: bordes e intermedios del nodo."""
    y_bottom = y_center - KEY_H / 2
    x_left = x_center - (n_keys * KEY_W) / 2
    return [
        [x_left + i * KEY_W, y_bottom, 0]
        for i in range(n_keys + 1)
    ]


class BTreeIntro(Scene):
    def construct(self):
        self.p1_multicamino()
        self.p2_ventaja()
        self.p3_comparacion()

    def p1_multicamino(self):
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
            nodo[0][0].get_left()[0] - 0.6,
            nodo[0][0].get_right()[0] - 0.20,
            nodo[0][1].get_right()[0] + 0.20,
            nodo[0][2].get_right()[0] + 0.6,
        ]
        etiq = VGroup(*[
            Text(txt, font_size=15, color=BLUE).move_to([x, -0.75, 0])
            for txt, x in zip(rangos, xs)
        ])
        self.play(LaggedStart(*[FadeIn(e, shift=UP) for e in etiq], lag_ratio=0.15),
                  run_time=1)

        msg = caption("3 claves → 4 hijos. Cada hijo cubre un rango.")
        self.play(Write(msg), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(VGroup(t, defi, nodo, etiq, msg)))

    def p2_ventaja(self):
        t = titulo("Un B-Tree de grado 4")
        self.play(Write(t), run_time=0.8)

        raiz = make_node([20, 40, 60], color=GREEN).move_to([0, 1.2, 0])
        hijos_pos = [-2.4, -0.8, 0.8, 2.4]
        hijos_keys = [[10], [30], [50], [70]]
        hijos = VGroup()
        for x, keys in zip(hijos_pos, hijos_keys):
            hijos.add(make_node(keys, color=GREEN).move_to([x, -0.6, 0]))

        lineas = VGroup()
        for start, child in zip(_start_points(0, 1.2, 3), hijos):
            lineas.add(Line(
                start=start,
                end=child.get_top(),
                color=GREEN, stroke_width=2,
            ))

        self.play(FadeIn(raiz), run_time=0.6)
        self.play(
            FadeIn(hijos),
            LaggedStart(*[Create(l) for l in lineas], lag_ratio=0.15),
            run_time=1.2,
        )

        msg = caption("7 claves en solo 2 niveles.")
        self.play(FadeIn(msg, shift=UP), run_time=0.6)
        self.wait(2)

        self.play(FadeOut(VGroup(t, raiz, hijos, lineas, msg)))

    def p3_comparacion(self):
        t = titulo("BST  vs  B-Tree")
        self.play(Write(t), run_time=0.8)

        # ---------- BST: 7 nodos ----------
        bst_lbl = Text("BST", font_size=26, color=BLUE).move_to([-4, 2.3, 0])

        bst_pos = {
            40: (-4.0,  1.5),
            20: (-5.2,  0.3),
            60: (-2.8,  0.3),
            10: (-5.8, -0.8),
            30: (-4.6, -0.8),
            50: (-3.4, -0.8),
            70: (-2.2, -0.8),
        }
        bst_nodos = {}
        for v, (x, y) in bst_pos.items():
            c = Circle(radius=0.22, color=BLUE, stroke_width=2)
            n = Text(str(v), font_size=14).move_to(c)
            bst_nodos[v] = VGroup(c, n).move_to([x, y, 0])

        bst_lin = VGroup(
            Line(bst_nodos[40].get_bottom(), bst_nodos[20].get_top(), color=BLUE, stroke_width=2),
            Line(bst_nodos[40].get_bottom(), bst_nodos[60].get_top(), color=BLUE, stroke_width=2),
            Line(bst_nodos[20].get_bottom(), bst_nodos[10].get_top(), color=BLUE, stroke_width=2),
            Line(bst_nodos[20].get_bottom(), bst_nodos[30].get_top(), color=BLUE, stroke_width=2),
            Line(bst_nodos[60].get_bottom(), bst_nodos[50].get_top(), color=BLUE, stroke_width=2),
            Line(bst_nodos[60].get_bottom(), bst_nodos[70].get_top(), color=BLUE, stroke_width=2),
        )

        # ---------- B-Tree: mismo ejemplo que la ventaja ----------
        bt_lbl = Text("B-Tree", font_size=26, color=GREEN).move_to([4, 2.3, 0])

        bt_raiz = make_node([20, 40, 60], color=GREEN).move_to([4, 1.5, 0])
        bt_hijos_pos = [1.6, 3.2, 4.8, 6.4]
        bt_hijos_keys = [[10], [30], [50], [70]]
        bt_hijos = VGroup()
        for x, keys in zip(bt_hijos_pos, bt_hijos_keys):
            bt_hijos.add(make_node(keys, color=GREEN).move_to([x, -0.3, 0]))

        bt_lin = VGroup()
        for start, child in zip(_start_points(4, 1.5, 3), bt_hijos):
            bt_lin.add(Line(
                start=start,
                end=child.get_top(),
                color=GREEN, stroke_width=2,
            ))

        # ---------- Animación ----------
        self.play(
            FadeIn(bst_lbl), FadeIn(bt_lbl),
            LaggedStart(*[FadeIn(n) for n in bst_nodos.values()], lag_ratio=0.05),
            LaggedStart(*[Create(l) for l in bst_lin], lag_ratio=0.05),
            FadeIn(bt_raiz),
            LaggedStart(*[FadeIn(h) for h in bt_hijos], lag_ratio=0.08),
            LaggedStart(*[Create(l) for l in bt_lin], lag_ratio=0.08),
            run_time=2,
        )

        eb = Text("7 claves · 3 niveles", font_size=18, color=BLUE).move_to([-4, -1.7, 0])
        et = Text("7 claves · 2 niveles", font_size=18, color=GREEN).move_to([4, -1.7, 0])
        self.play(FadeIn(eb), FadeIn(et), run_time=0.6)

        cierre = caption("Mismas claves, menos niveles, menos accesos a disco.")
        self.play(Write(cierre), run_time=0.8)
        self.wait(2.5)

        self.play(FadeOut(VGroup(
            t, bst_lbl, *bst_nodos.values(), bst_lin,
            bt_lbl, bt_raiz, bt_hijos, bt_lin,
            eb, et, cierre,
        )))