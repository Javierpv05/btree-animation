# Escena 6a: Split en inserción
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import titulo, caption, make_node, switch_caption


class BTreeSplitInsercion(Scene):
    def construct(self):
        t = titulo("Split en Inserción")
        self.play(Write(t), run_time=1.5)
        self.wait(1.0)

        # Nodo raíz inicial
        n = make_node([10, 20], color=GREEN).move_to([0, 0.8, 0])
        self.play(FadeIn(n), run_time=1.0)
        cap = caption("Nodo lleno: [10, 20] (máximo 2 claves para m=3).")
        self.play(FadeIn(cap, shift=UP), run_time=1.0)
        self.wait(2.0)

        # Insertar 30 -> overflow
        new_cap = caption("Insertar 30 → el nodo se desborda.")
        self.play(*switch_caption(cap, new_cap), run_time=1.0)
        cap = new_cap
        n_over = make_node([10, 20, 30], color=RED).move_to([0, 0.8, 0])
        self.play(Transform(n, n_over), run_time=1.5)
        self.play(Indicate(n_over, color=RED), run_time=1.0)
        self.wait(2.0)

        # Split
        new_cap = caption("Split: sube 20 al padre y el nodo se divide.")
        self.play(*switch_caption(cap, new_cap), run_time=1.0)
        cap = new_cap
        self.play(FadeOut(n), run_time=1.0)
        self.wait(1.0)

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
            run_time=2.0,
        )
        self.wait(2.5)

        # Insertar 5
        new_cap = caption("Insertar 5 → baja a la hoja [10].")
        self.play(*switch_caption(cap, new_cap), run_time=1.0)
        cap = new_cap
        izq_v2 = make_node([5, 10], color=GREEN).move_to([-1.6, -0.2, 0])
        l1_v2 = _line(root, izq_v2)
        self.play(
            FadeOut(izq), FadeOut(l1),
            FadeIn(izq_v2), Create(l1_v2),
            run_time=1.5,
        )
        izq = izq_v2
        l1 = l1_v2
        self.wait(2.0)

        # Insertar 15 -> overflow
        new_cap = caption("Insertar 15 → la hoja se desborda.")
        self.play(*switch_caption(cap, new_cap), run_time=1.0)
        cap = new_cap
        izq_over = make_node([5, 10, 15], color=RED).move_to([-1.6, -0.2, 0])
        self.play(Transform(izq, izq_over), run_time=1.5)
        self.play(Indicate(izq_over, color=RED), run_time=1.0)
        self.wait(2.0)

        # Split de hoja
        new_cap = caption("Split: 10 sube al padre → raíz [10, 20].")
        self.play(*switch_caption(cap, new_cap), run_time=1.0)
        cap = new_cap
        self.play(FadeOut(izq), run_time=1.0)
        self.wait(1.0)

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
            run_time=2.0,
        )
        self.wait(3.0)

        cierre = caption("Resultado: raíz [10, 20], hijos [5], [15], [30].")
        self.play(*switch_caption(cap, cierre), run_time=1.0)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)


class BTreeMergeEliminacion(Scene):
    def construct(self):
        t = titulo("Merge en Eliminación")
        self.play(Write(t), run_time=1.5)
        self.wait(1.0)

        # Árbol inicial: raíz [10,20], hijos [5], [15], [30]
        root = make_node([10, 20], color=GREEN).move_to([0, 1.6, 0])
        h1 = make_node([5], color=GREEN).move_to([-2.6, -0.2, 0])
        h2 = make_node([15], color=GREEN).move_to([0.0, -0.2, 0])
        h3 = make_node([30], color=GREEN).move_to([2.6, -0.2, 0])

        def _line(p, c):
            return Line(p.get_bottom(), c.get_top(), color=GREEN, stroke_width=2)

        l1 = _line(root, h1)
        l2 = _line(root, h2)
        l3 = _line(root, h3)
        lin = VGroup(l1, l2, l3)

        self.play(
            FadeIn(root), FadeIn(h1), FadeIn(h2), FadeIn(h3),
            LaggedStart(*[Create(l) for l in lin], lag_ratio=0.2),
            run_time=2.0,
        )
        cap = caption("Árbol inicial: raíz [10, 20], hijos [5], [15], [30].")
        self.play(FadeIn(cap, shift=UP), run_time=1.0)
        self.wait(2.5)

        # --- PASO 1: Eliminar 30 ---
        new_cap = caption("Paso 1: Eliminar 30 → la hoja [30] queda vacía (underflow).")
        self.play(*switch_caption(cap, new_cap), run_time=1.0)
        cap = new_cap
        self.play(h3[0].animate.set_color(RED), run_time=1.0)
        self.play(Indicate(h3, color=RED), run_time=1.0)
        self.wait(1.0)
        
        # Desaparecer el nodo 30
        self.play(FadeOut(h3), FadeOut(l3), run_time=1.5)
        self.wait(1.5)

        # --- PASO 2: Bajar el 20 del padre ---
        new_cap = caption("Paso 2: El 20 del padre baja para fusionarse con [15].")
        self.play(*switch_caption(cap, new_cap), run_time=1.0)
        cap = new_cap
        self.wait(1.0)

        # Transformamos la raíz para quitarle el 20
        root_final = make_node([10], color=GREEN).move_to([0, 1.6, 0])
        
        # Transformamos el nodo [15] para que ahora sea [15, 20]
        h2_merged = make_node([15, 20], color=GREEN).move_to([0.0, -0.2, 0])
        
        # Creamos las líneas nuevas
        l1_final = _line(root_final, h1)
        l2_final = _line(root_final, h2_merged)

        self.play(
            Transform(root, root_final),
            Transform(h2, h2_merged),
            Transform(l1, l1_final),
            Transform(l2, l2_final),
            run_time=2.5,
        )
        self.wait(2.0)

        # --- PASO 3: Mostrar resultado ---
        new_cap = caption("Resultado: raíz [10], hijos [5] y [15, 20].")
        self.play(*switch_caption(cap, new_cap), run_time=1.0)
        cap = new_cap
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)