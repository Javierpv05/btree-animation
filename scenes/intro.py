"""Escena 1: título, autores, curso."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import Y_CAPTION, FS_SUBTITULO, FS_TEXTO, FS_ETIQUETA


TITULO_PROYECTO = "B-Trees"
CURSO           = "CS2023 — Algoritmos y Estructuras de Datos"
INTEGRANTES     = ["Javier pariansullca ventura", "Ernesto sullca toledo", "Integrante 3"]
FECHA           = "Septiembre 2026"
UNIVERSIDAD     = "Universidad / Institución"


class Intro(Scene):
    def construct(self):
        titulo = Text(TITULO_PROYECTO, font_size=96, color=GREEN, weight=BOLD)
        linea  = Line(LEFT * 5, RIGHT * 5, color=GREEN, stroke_width=2
                     ).next_to(titulo, DOWN, buff=0.4)

        self.play(Write(titulo), run_time=1)
        self.play(Create(linea), run_time=0.4)

        sub = Text(CURSO, font_size=FS_SUBTITULO).next_to(linea, DOWN, buff=0.5)
        self.play(FadeIn(sub, shift=UP), run_time=0.6)

        nombres = VGroup(*[
            Text(n, font_size=FS_TEXTO) for n in INTEGRANTES
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(sub, DOWN, buff=0.6)
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT) for n in nombres],
                              lag_ratio=0.2), run_time=0.8)

        pie = Text(f"{UNIVERSIDAD} · {FECHA}",
                   font_size=FS_ETIQUETA, color=GREY_B
                  ).move_to([0, Y_CAPTION, 0])
        self.play(FadeIn(pie), run_time=0.4)
        self.wait(1.2)

        self.play(FadeOut(VGroup(titulo, linea, sub, nombres, pie)), run_time=0.6)