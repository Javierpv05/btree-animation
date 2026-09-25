# Escena 9: cierre.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *


class Outro(Scene):
    def construct(self):
        gracias = Text("Gracias", font_size=80, color=GREEN, weight=BOLD)
        self.play(Write(gracias), run_time=1)

        curso = Text("CS2023 — Algoritmos y Estructuras de Datos",
                     font_size=24).next_to(gracias, DOWN, buff=0.5)
        self.play(FadeIn(curso, shift=UP), run_time=0.6)
        self.wait(1.5)

        self.play(FadeOut(VGroup(gracias, curso)))