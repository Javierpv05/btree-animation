"""
Escena 7: Split y Merge (secuencial).

Flujo:
    1. Insertar claves hasta que un nodo se desborde.
    2. Split: la clave media sube, el nodo se divide.
    3. Insertar más claves para ver el árbol crecer.
    4. Eliminar una clave para forzar un merge.
    5. Resultado final.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import titulo, caption, make_node, switch_caption


class BTreeSplit(Scene):
    def construct(self):
        t = titulo("Split y Merge")
        self.play(Write(t), run_time=0.8)
        self.wait(0.3)

        # ---------------------------------------------------
        # PASO 1: nodo lleno [10, 20]
        # ---------------------------------------------------
        n = make_node([10, 20], color=GREEN).move_to([0, 0.8, 0])
        self.play(FadeIn(n), run_time=0.5)

        cap = caption("Nodo lleno: [10, 20]  (máximo 2 claves para m = 3).")
        self.play(FadeIn(cap, shift=UP), run_time=0.5)
        self.wait(1.5)

        # ---------------------------------------------------
        # PASO 2: insertar 30 → desbordamiento (rojo)
        # ---------------------------------------------------
        new_cap = caption("Insertar 30  →  el nodo se desborda.")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        n_over = make_node([10, 20, 30], color=RED).move_to([0, 0.8, 0])
        self.play(Transform(n, n_over), run_time=0.7)
        self.wait(1.2)

        # ---------------------------------------------------
        # PASO 3: split — el rojo desaparece por completo
        # ---------------------------------------------------
        new_cap = caption("Split: sube 20 al padre y el nodo se divide.")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        # Desvanecemos el nodo rojo ANTES de dibujar el resultado
        self.play(FadeOut(n), run_time=0.4)
        self.wait(0.3)

        root = make_node([20], color=GREEN).move_to([0, 1.6, 0])
        izq = make_node([10], color=GREEN).move_to([-1.6, -0.2, 0])
        der = make_node([30], color=GREEN).move_to([1.6, -0.2, 0])

        def _line(p, c):
            return Line(p.get_bottom(), c.get_top(), color=GREEN, stroke_width=2)

        l1 = _line(root, izq)
        l2 = _line(root, der)

        self.play(
            FadeIn(root), FadeIn(izq), FadeIn(der),
            Create(l1), Create(l2),
            run_time=1,
        )
        self.wait(1.5)

        # ---------------------------------------------------
        # PASO 4: insertar 5 en la hoja [10]
        # ---------------------------------------------------
        new_cap = caption("Insertar 5  →  baja a la hoja [10].")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        izq_v2 = make_node([5, 10], color=GREEN).move_to([-1.6, -0.2, 0])
        l1_v2 = _line(root, izq_v2)

        self.play(
            FadeOut(izq), FadeOut(l1),
            FadeIn(izq_v2), Create(l1_v2),
            run_time=0.8,
        )
        izq = izq_v2
        l1 = l1_v2
        self.wait(1.2)

        # ---------------------------------------------------
        # PASO 5: insertar 15 → la hoja se desborda
        # ---------------------------------------------------
        new_cap = caption("Insertar 15  →  la hoja se desborda.")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        izq_over = make_node([5, 10, 15], color=RED).move_to([-1.6, -0.2, 0])
        self.play(Transform(izq, izq_over), run_time=0.7)
        self.wait(1.2)

        # ---------------------------------------------------
        # PASO 6: split del hijo → nueva raíz [10, 20]
        # ---------------------------------------------------
        new_cap = caption("Split: 10 sube al padre  →  raíz [10, 20].")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        # Quitar el rojo antes de dibujar el nuevo árbol
        self.play(FadeOut(izq), run_time=0.4)
        self.wait(0.3)

        root_new = make_node([10, 20], color=GREEN).move_to([0, 1.6, 0])
        h1 = make_node([5], color=GREEN).move_to([-2.6, -0.2, 0])
        h2 = make_node([15], color=GREEN).move_to([0.0, -0.2, 0])
        h3 = make_node([30], color=GREEN).move_to([2.6, -0.2, 0])

        lin_new = VGroup(
            _line(root_new, h1),
            _line(root_new, h2),
            _line(root_new, h3),
        )

        self.play(
            FadeOut(VGroup(root, l1, l2)),
            FadeIn(root_new),
            FadeIn(h1), FadeIn(h2), FadeIn(h3),
            LaggedStart(*[Create(l) for l in lin_new], lag_ratio=0.2),
            run_time=1.2,
        )
        self.wait(1.5)

        # ---------------------------------------------------
        # PASO 7: eliminar 30 → merge
        # ---------------------------------------------------
        new_cap = caption("Eliminar 30  →  la hoja queda vacía, merge con el padre.")
        self.play(*switch_caption(cap, new_cap), run_time=0.5)
        cap = new_cap

        # Resaltar el nodo a eliminar
        self.play(h3[0].animate.set_color(RED), run_time=0.4)
        self.wait(0.8)

        # Merge: [15] + 20 + [] → [15, 20]; padre [10, 20] → [10]
        root_fin = make_node([10], color=GREEN).move_to([0, 1.6, 0])
        h1_fin = make_node([5], color=GREEN).move_to([-1.6, -0.2, 0])
        h2_fin = make_node([15, 20], color=GREEN).move_to([1.6, -0.2, 0])

        lin_fin = VGroup(
            _line(root_fin, h1_fin),
            _line(root_fin, h2_fin),
        )

        self.play(
            FadeOut(VGroup(root_new, h1, h2, h3, lin_new)),
            FadeIn(root_fin), FadeIn(h1_fin), FadeIn(h2_fin),
            LaggedStart(*[Create(l) for l in lin_fin], lag_ratio=0.3),
            run_time=1.2,
        )
        self.wait(1.5)

        # ---------------------------------------------------
        # CIERRE
        # ---------------------------------------------------
        cierre = caption("Resultado: raíz [10], hijos [5] y [15, 20].")
        self.play(*switch_caption(cap, cierre), run_time=0.6)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)