# Escena 2: qué es un BST, versión corta.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import FS_TEXTO, titulo, caption


class BSTIntro(Scene):
    def construct(self):
        t = titulo("Antes: el BST")
        self.play(Write(t), run_time=0.8)

        defi = Text(
            "Árbol binario: 1 clave por nodo, máximo 2 hijos.",
            font_size=FS_TEXTO,
        ).move_to([0, 2, 0])
        self.play(FadeIn(defi, shift=UP), run_time=0.6)
        self.wait(0.8)

        pos = {
            50: (0, 0.7),
            30: (-1.5, -0.3),
            70: (1.5, -0.3),
            20: (-2.3, -1.3),
            40: (-0.7, -1.3),
            60: (0.7, -1.3),
            80: (2.3, -1.3),
        }

        nodos = {}
        for v, (x, y) in pos.items():
            c = Circle(radius=0.28, color=BLUE, stroke_width=2)
            n = Text(str(v), font_size=18).move_to(c)
            nodos[v] = VGroup(c, n).move_to([x, y, 0])

        lineas = VGroup(
            Line(nodos[50].get_bottom(), nodos[30].get_top(), color=BLUE, stroke_width=2),
            Line(nodos[50].get_bottom(), nodos[70].get_top(), color=BLUE, stroke_width=2),
            Line(nodos[30].get_bottom(), nodos[20].get_top(), color=BLUE, stroke_width=2),
            Line(nodos[30].get_bottom(), nodos[40].get_top(), color=BLUE, stroke_width=2),
            Line(nodos[70].get_bottom(), nodos[60].get_top(), color=BLUE, stroke_width=2),
            Line(nodos[70].get_bottom(), nodos[80].get_top(), color=BLUE, stroke_width=2),
        )

        self.play(
            LaggedStart(*[FadeIn(n) for n in nodos.values()], lag_ratio=0.06),
            LaggedStart(*[Create(l) for l in lineas], lag_ratio=0.06),
            run_time=1.2,
        )
        self.wait(0.8)

        gancho = caption("¿Qué pasa si se desbalancea?")
        self.play(Write(gancho), run_time=0.8)
        self.wait(1.2)

        self.play(FadeOut(VGroup(t, defi, *nodos.values(), lineas, gancho)))