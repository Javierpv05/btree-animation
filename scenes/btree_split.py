# Escena 6: split en inserción (izquierda) y merge en eliminación (derecha).
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import (
    titulo, caption, make_node, switch_caption,
)


CENTRO_IZQ = -3.5
CENTRO_DER =  3.5


class BTreeSplit(Scene):
    def construct(self):
        t = titulo("Split  vs  Merge")
        self.play(Write(t), run_time=0.8)
        self.wait(0.3)

        divider = DashedLine(
            [0, 2.4, 0], [0, -2.5, 0],
            color=GREY_B, stroke_width=2,
        )
        self.play(Create(divider), run_time=0.5)

        izq_lbl = Text("Split (inserción)", font_size=24, color=GREEN
                      ).move_to([CENTRO_IZQ, 1.9, 0])
        der_lbl = Text("Merge (eliminación)", font_size=24, color=RED
                      ).move_to([CENTRO_DER, 1.9, 0])
        self.play(Write(izq_lbl), Write(der_lbl), run_time=0.6)
        self.wait(0.4)

        cap = caption("Ambos lados: un nodo lleno [10, 20].")
        self.play(FadeIn(cap, shift=UP), run_time=0.5)

        n_izq = make_node([10, 20], color=GREEN).move_to([CENTRO_IZQ, 0.4, 0])
        n_der = make_node([10, 20], color=GREEN).move_to([CENTRO_DER, 0.4, 0])

        self.play(FadeIn(n_izq), FadeIn(n_der), run_time=0.8)
        self.wait(1.5)

        new_cap = caption("Izquierda: insertar 30  →  overflow.")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        n_izq_over = make_node([10, 20, 30], color=RED).move_to([CENTRO_IZQ, 0.4, 0])
        self.play(Transform(n_izq, n_izq_over), run_time=0.7)
        self.play(Indicate(n_izq, color=RED, scale_factor=1.08), run_time=0.6)
        self.wait(1.0)

        new_cap = caption("Split: la clave media 20 sube al padre.")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        self.play(FadeOut(n_izq), run_time=0.5)
        self.wait(0.3)

        raiz_izq = make_node([20], color=YELLOW).move_to([CENTRO_IZQ, 1.4, 0])
        izq1 = make_node([10], color=GREEN).move_to([CENTRO_IZQ - 1.1, -0.2, 0])
        izq2 = make_node([30], color=GREEN).move_to([CENTRO_IZQ + 1.1, -0.2, 0])

        def _line(p, c, color=GREEN):
            return Line(p.get_bottom(), c.get_top(), color=color, stroke_width=2)

        l1 = _line(raiz_izq, izq1, color=YELLOW)
        l2 = _line(raiz_izq, izq2, color=YELLOW)

        self.play(
            FadeIn(raiz_izq), FadeIn(izq1), FadeIn(izq2),
            Create(l1), Create(l2),
            run_time=1.0,
        )
        self.play(Indicate(raiz_izq, color=YELLOW, scale_factor=1.1), run_time=0.7)
        self.wait(1.5)

        self.play(raiz_izq[0].animate.set_color(GREEN), run_time=0.3)

        new_cap = caption("Derecha: mismo árbol, ahora con 3 claves en las hojas.")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        self.play(FadeOut(n_der), run_time=0.4)
        self.wait(0.3)

        raiz_der = make_node([20], color=GREEN).move_to([CENTRO_DER, 1.4, 0])
        der1 = make_node([10], color=GREEN).move_to([CENTRO_DER - 1.1, -0.2, 0])
        der2 = make_node([30], color=GREEN).move_to([CENTRO_DER + 1.1, -0.2, 0])

        l3 = _line(raiz_der, der1)
        l4 = _line(raiz_der, der2)

        self.play(
            FadeIn(raiz_der), FadeIn(der1), FadeIn(der2),
            Create(l3), Create(l4),
            run_time=1.0,
        )
        self.wait(1.5)

        new_cap = caption("Eliminar 30  →  la hoja queda vacía (underflow).")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        self.play(der2[0].animate.set_color(RED), run_time=0.4)
        self.play(Indicate(der2, color=RED, scale_factor=1.1), run_time=0.6)
        self.wait(0.6)

        self.play(FadeOut(der2), FadeOut(l4), run_time=0.5)
        self.wait(0.6)

        new_cap = caption("Merge: 20 baja del padre y se une a [10].")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        nodo_fusionado = make_node([10, 20], color=GREEN).move_to([CENTRO_DER, 0.4, 0])

        self.play(
            FadeOut(raiz_der), FadeOut(der1), FadeOut(l3),
            FadeIn(nodo_fusionado, scale=0.9),
            run_time=1.2,
        )
        self.wait(1.5)

        new_cap = caption("La raíz queda vacía  →  baja un nivel.")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        self.play(nodo_fusionado.animate.move_to([CENTRO_DER, 0.4, 0]),
                  run_time=0.5)
        self.wait(1.2)

        new_cap = caption("Split hace crecer el árbol hacia arriba.  Merge lo contrae.")
        self.play(*switch_caption(cap, new_cap), run_time=0.6)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)