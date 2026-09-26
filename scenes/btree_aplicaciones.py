# Escena 8: por qué importa (RAM vs disco) y aplicaciones reales.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import FS_TEXTO, titulo, caption


class BTreeAplicaciones(Scene):
    def construct(self):
        t = titulo("¿Por qué importa el B-Tree?")
        self.play(Write(t), run_time=0.8)

        ram = Rectangle(width=4, height=1.0, color=BLUE, stroke_width=2).move_to([-3.5, 0.8, 0])
        ram_txt = Text("RAM  ~100 ns", font_size=22, color=BLUE).move_to(ram)
        disco = Rectangle(width=4, height=1.0, color=RED, stroke_width=2).move_to([-3.5, -0.7, 0])
        disco_txt = Text("Disco  ~10 ms", font_size=22, color=RED).move_to(disco)
        factor = Text("~100,000× más lento", font_size=22, color=YELLOW).move_to([3.0, 0, 0])

        self.play(FadeIn(ram), FadeIn(ram_txt), run_time=0.5)
        self.play(FadeIn(disco), FadeIn(disco_txt), run_time=0.5)
        self.play(FadeIn(factor, shift=LEFT), run_time=0.5)
        self.wait(2)

        self.play(FadeOut(VGroup(t, ram, ram_txt, disco, disco_txt, factor)))

        t2 = titulo("Aplicaciones reales")
        self.play(Write(t2), run_time=0.8)

        apps = [
            ("Bases de datos",       "MySQL, PostgreSQL, SQLite usan B+Trees."),
            ("Sistemas de archivos", "NTFS, ext4, Btrfs organizan con B-Trees."),
            ("Motores de búsqueda",  "Lucene / Elasticsearch usan estructuras derivadas."),
            ("Sistemas embebidos",   "SQLite en móviles y navegadores."),
        ]

        grupo = VGroup()
        for nom, desc in apps:
            grupo.add(VGroup(
                Text("•  " + nom, font_size=26, color=GREEN),
                Text(desc, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1))

        grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0, 0])

        self.play(LaggedStart(*[FadeIn(g, shift=RIGHT) for g in grupo], lag_ratio=0.25),
                  run_time=1.8)
        self.wait(1.5)

        cierre = caption("Cada búsqueda en una base de datos usa un B-Tree.")
        self.play(Write(cierre), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(VGroup(t2, grupo, cierre)))