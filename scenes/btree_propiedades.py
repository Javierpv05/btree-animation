# Escena 5: propiedades, reglas por tipo de nodo y complejidades.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import *
from utils.btree_layout import (
    FS_TEXTO, titulo, caption,
    tabla_columnas, linea_tabla,
)


class BTreePropiedades(Scene):
    def construct(self):
        self.p1_grado()
        self.p2_reglas()
        self.p3_balance()
        self.p4_complejidad()

    def p1_grado(self):
        t = titulo("Propiedades del B-Tree")
        self.play(Write(t), run_time=0.8)

        grado = Text("Grado  m  = máximo de hijos por nodo.",
                     font_size=FS_TEXTO, color=YELLOW).move_to([0, 2, 0])
        self.play(FadeIn(grado, shift=UP), run_time=0.6)

        rel = VGroup(
            Text("máximo de claves  =  m - 1", font_size=FS_TEXTO),
            Text("mínimo de claves  =  ⌈m/2⌉ - 1", font_size=FS_TEXTO),
            Text("mínimo de hijos   =  ⌈m/2⌉", font_size=FS_TEXTO),
        ).arrange(DOWN, buff=0.25).next_to(grado, DOWN, buff=0.5)

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT) for r in rel], lag_ratio=0.2),
                  run_time=1)
        self.wait(2)
        self.play(FadeOut(VGroup(t, grado, rel)))

    def p2_reglas(self):
        t = titulo("Reglas por tipo de nodo")
        self.play(Write(t), run_time=0.8)

        COL_XS = [-5.5, -3.0, -1.0, 1.5, 4.0]

        headers, filas = tabla_columnas(
            columnas_x=COL_XS,
            headers=["Tipo de nodo", "Claves mín", "Claves máx", "Hijos mín", "Hijos máx"],
            filas=[
                ["Nodo raíz",           "1",         "m - 1", "2",     "m"],
                ["Nodo hijo (no hoja)", "⌈m/2⌉ - 1", "m - 1", "⌈m/2⌉", "m"],
                ["Nodo hoja",           "⌈m/2⌉ - 1", "m - 1", "0",     "0"],
            ],
            y_header=1.6, y_inicio=0.9, dy=0.6,
            fs_header=20, fs_fila=18,
            colores_fila=lambda i, j: (
                WHITE if j == 0
                else (BLUE if j in (1, 3) else GREEN)
            ),
        )
        linea = linea_tabla(y=1.35, ancho=6.5)

        self.play(FadeIn(headers), Create(linea), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(f, shift=RIGHT) for f in filas], lag_ratio=0.08),
            run_time=1.2,
        )
        self.wait(2.5)

        ej = Text(
            "Ejemplo (m = 3):  hijo no-raíz tiene 1 clave y 2 o 3 hijos.",
            font_size=20, color=YELLOW,
        ).move_to([0, -2.7, 0])
        self.play(FadeIn(ej, shift=UP), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(VGroup(t, headers, linea, filas, ej)))

    def p3_balance(self):
        t = titulo("Balance garantizado")
        self.play(Write(t), run_time=0.8)

        def nodo(keys, X, Y):
            cajas = VGroup(*[
                Rectangle(width=0.7, height=0.7, color=GREEN, stroke_width=2)
                for _ in keys
            ]).arrange(RIGHT, buff=0)
            textos = VGroup(*[
                Text(str(k), font_size=18).move_to(c)
                for k, c in zip(keys, cajas)
            ])
            return VGroup(cajas, textos).move_to([X, Y, 0])

        raiz = nodo([14], 0, 1.8)
        internos = VGroup(nodo([7], -1.8, 0.3), nodo([20], 1.8, 0.3))
        hojas = VGroup(
            nodo([3, 5], -2.7, -1.3), nodo([10, 12], -0.9, -1.3),
            nodo([17, 18], 0.9, -1.3), nodo([25, 30], 2.7, -1.3),
        )
        lineas = VGroup(
            Line(raiz.get_bottom(), internos[0].get_top(), color=GREEN, stroke_width=2),
            Line(raiz.get_bottom(), internos[1].get_top(), color=GREEN, stroke_width=2),
            Line(internos[0].get_bottom(), hojas[0].get_top(), color=GREEN, stroke_width=2),
            Line(internos[0].get_bottom(), hojas[1].get_top(), color=GREEN, stroke_width=2),
            Line(internos[1].get_bottom(), hojas[2].get_top(), color=GREEN, stroke_width=2),
            Line(internos[1].get_bottom(), hojas[3].get_top(), color=GREEN, stroke_width=2),
        )
        self.play(FadeIn(raiz), FadeIn(internos), FadeIn(hojas),
                  LaggedStart(*[Create(l) for l in lineas], lag_ratio=0.1),
                  run_time=1.5)

        linea_nivel = DashedLine([-5, -2, 0], [5, -2, 0],
                                 color=YELLOW, stroke_width=2, dash_length=0.12)
        lbl = Text("todas al mismo nivel", font_size=18, color=YELLOW
                  ).next_to(linea_nivel, DOWN, buff=0.1)
        self.play(Create(linea_nivel), FadeIn(lbl), run_time=0.6)

        msg = caption("Nunca hay hojas a distinta profundidad.")
        self.play(Write(msg), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(VGroup(t, raiz, internos, hojas, lineas,
                                  linea_nivel, lbl, msg)))

    def p4_complejidad(self):
        t = titulo("Complejidades")
        self.play(Write(t), run_time=0.8)

        COL_XS = [-5.0, -2.0, 1.5, 5.0]
        headers, filas = tabla_columnas(
            columnas_x=COL_XS,
            headers=["Estructura", "Buscar", "Insertar", "Eliminar"],
            filas=[
                ["BST degenerado",   "O(n)",       "O(n)",       "O(n)"],
                ["BST balanceado",   "O(log n)",   "O(log n)",   "O(log n)"],
                ["B-Tree (grado m)", "O(logₘ n)",  "O(logₘ n)",  "O(logₘ n)"],
            ],
            y_header=1.5, y_inicio=0.7, dy=0.6,
            fs_header=22, fs_fila=20,
            colores_fila=lambda i, j: (
                WHITE if j == 0
                else (RED if i == 0 else BLUE if i == 1 else GREEN)
            ),
        )
        linea = linea_tabla(y=1.2, ancho=6.0)

        self.play(FadeIn(headers), Create(linea), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(f, shift=RIGHT) for f in filas], lag_ratio=0.1),
            run_time=1.5,
        )
        self.wait(2)

        nota = Text("Altura:  h ≤ log_m ( (n+1)/2 )",
                    font_size=24, color=YELLOW).move_to([0, -2.0, 0])
        self.play(Write(nota), run_time=1)
        self.wait(2)

        cierre = caption("Con m grande, la altura es mínima.")
        self.play(Write(cierre), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(VGroup(t, headers, linea, filas, nota, cierre)))