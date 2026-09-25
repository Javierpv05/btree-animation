"""Escena 5: por qué importa el B-Tree (jerarquía de memoria)."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import FS_TEXTO, titulo, caption


class BTreeVentaja(Scene):
    def construct(self):
        t = titulo("La ventaja del B-Tree")
        self.play(Write(t), run_time=0.8)

        ram = Rectangle(width=4, height=1.1, color=BLUE, stroke_width=2).move_to([-3, 1.2, 0])
        ram_txt = Text("RAM  ~100 ns", font_size=22, color=BLUE).move_to(ram)
        disco = Rectangle(width=4, height=1.1, color=RED, stroke_width=2).move_to([-3, -0.5, 0])
        disco_txt = Text("Disco  ~10 ms", font_size=22, color=RED).move_to(disco)
        factor = Text("~100,000× más lento", font_size=22, color=YELLOW).move_to([3.5, 0.3, 0])

        self.play(FadeIn(ram), FadeIn(ram_txt), run_time=0.5)
        self.play(FadeIn(disco), FadeIn(disco_txt), run_time=0.5)
        self.play(FadeIn(factor, shift=LEFT), run_time=0.5)
        self.wait(1.5)

        self.play(FadeOut(VGroup(ram, ram_txt, disco, disco_txt, factor)))

        # Comparativa de altura
        titulo2 = Text("Con 10⁹ claves:", font_size=24).move_to([0, 2, 0])
        self.play(FadeIn(titulo2))

        rows = VGroup(
            Text("BST balanceado → altura ≈ 30", font_size=24, color=RED),
            Text("B-Tree (m=100) → altura ≤ 4", font_size=24, color=GREEN),
            Text("B-Tree (m=1000) → altura ≤ 3", font_size=24, color=GREEN),
        ).arrange(DOWN, buff=0.35).next_to(titulo2, DOWN, buff=0.5)

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT) for r in rows], lag_ratio=0.2),
                  run_time=1)
        self.wait(1.5)

        cierre = caption("Menos altura = menos accesos a disco.")
        self.play(Write(cierre), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(VGroup(titulo2, rows, cierre, t)))