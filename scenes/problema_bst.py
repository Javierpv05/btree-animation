# Escena 3: problema del BST con tabla de complejidades.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import (
    FS_TEXTO, titulo, caption,
    tabla_columnas, linea_tabla,
)


class ProblemaBST(Scene):
    def construct(self):
        t = titulo("El problema con un BST")
        self.play(Write(t), run_time=0.8)

        intro = Text(
            "Un BST sin balancear puede degenerar en una lista.",
            font_size=FS_TEXTO,
        ).move_to([0, 2, 0])
        self.play(FadeIn(intro, shift=UP), run_time=0.6)
        self.wait(0.8)

        COL_XS = [-4.0, -1.0, 2.0]
        headers, filas = tabla_columnas(
            columnas_x=COL_XS,
            headers=["Operación", "Balanceado", "Degenerado"],
            filas=[
                ["Buscar",   "O(log n)", "O(n)"],
                ["Insertar", "O(log n)", "O(n)"],
                ["Eliminar", "O(log n)", "O(n)"],
            ],
            y_header=1.0,
            y_inicio=0.3,
            dy=0.55,
            colores_fila=lambda i, j: (
                WHITE if j == 0 else (BLUE if j == 1 else RED)
            ),
        )
        linea = linea_tabla(y=0.65, ancho=5.5)

        self.play(FadeIn(headers), Create(linea), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(f, shift=RIGHT) for f in filas], lag_ratio=0.1),
            run_time=1,
        )
        self.wait(1.5)

        cierre = caption("Necesitamos algo más ancho y balanceado.")
        self.play(Write(cierre), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(VGroup(t, intro, headers, linea, filas, cierre)))