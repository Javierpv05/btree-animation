"""Escena 10: aplicaciones reales."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import FS_TEXTO, titulo, caption


class BTreeAplicaciones(Scene):
    def construct(self):
        t = titulo("Aplicaciones reales")
        self.play(Write(t), run_time=0.8)

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

        self.play(FadeOut(VGroup(t, grupo, cierre)))