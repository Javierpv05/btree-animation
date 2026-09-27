import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from manim import *

from utils.btree import BTree
from utils.btree_layout import (
    caption,
    tree_to_vgroup,
    switch_caption,
)


DEGREE = 3

KEYS_INSERT = [
    10, 20, 5, 6, 12, 30, 7, 17
]

KEYS_DELETE = [
    6, 30
]

KEY_SEARCH = 7


class BTreeEjemplo(Scene):

    def construct(self):

        title = Text(
            f"Ejemplo: B-Tree de grado m = {DEGREE}",
            font_size=34,
            color=GREEN,
        ).to_edge(
            UP,
            buff=0.35,
        )

        self.play(
            Write(title),
            run_time=0.8,
        )

        tree = BTree(
            degree=DEGREE,
        )

        cur = None
        cap = None

        # =========================================================
        # INSERCIÓN
        # =========================================================

        label = self.keys_label(
            KEYS_INSERT,
            "Insertar:",
            YELLOW,
        )

        self.play(
            FadeIn(
                label,
                shift=RIGHT * 0.25,
            ),
            run_time=0.5,
        )

        self.wait(0.5)

        for key in KEYS_INSERT:

            cur, cap = self.animate_steps(
                tree.insert_with_steps(key),
                cur,
                cap,
                operation="insert",
            )

        self.play(
            FadeOut(label),
            run_time=0.4,
        )

        self.wait(0.6)

        # =========================================================
        # ELIMINACIÓN
        # =========================================================

        label = self.keys_label(
            KEYS_DELETE,
            "Eliminar:",
            RED,
        )

        self.play(
            FadeIn(
                label,
                shift=RIGHT * 0.25,
            ),
            run_time=0.5,
        )

        self.wait(0.5)

        for key in KEYS_DELETE:

            cur, cap = self.animate_steps(
                tree.delete_with_steps(key),
                cur,
                cap,
                operation="delete",
            )

            self.wait(0.5)

        self.play(
            FadeOut(label),
            run_time=0.4,
        )

        # =========================================================
        # BÚSQUEDA
        # =========================================================

        label = self.keys_label(
            [KEY_SEARCH],
            "Buscar:",
            BLUE,
        )

        self.play(
            FadeIn(
                label,
                shift=RIGHT * 0.25,
            ),
            run_time=0.5,
        )

        self.wait(0.5)

        cur, cap = self.animate_steps(
            tree.search_with_steps(KEY_SEARCH),
            cur,
            cap,
            operation="search",
        )

        self.play(
            FadeOut(label),
            run_time=0.4,
        )

        # =========================================================
        # FINAL
        # =========================================================

        final = caption(
            "B-Tree: insertar, eliminar y buscar "
            "en O(log n)."
        )

        self.play(
            *switch_caption(
                cap,
                final,
            ),
            run_time=0.8,
        )

        cap = final

        self.wait(2)

    # =============================================================
    # ANIMACIÓN GENÉRICA DE PASOS
    # =============================================================

    def animate_steps(
        self,
        steps,
        cur,
        cap,
        operation,
    ):

        for step in steps:

            new_tree = tree_to_vgroup(
                step.tree,
                highlight_path=step.highlight_path,
            )

            new_cap = caption(
                step.caption,
            )

            if cur is None:

                cur = new_tree
                cap = new_cap

                self.play(
                    FadeIn(
                        cur,
                        shift=UP * 0.12,
                    ),
                    FadeIn(
                        cap,
                        shift=UP * 0.12,
                    ),
                    run_time=0.8,
                )

            else:

                self.play(
                    Transform(
                        cur,
                        new_tree,
                    ),
                    *switch_caption(
                        cap,
                        new_cap,
                    ),
                    run_time=self.animation_time(
                        step.caption,
                        operation,
                    ),
                )

                cap = new_cap

            self.wait(
                self.pause_time(
                    step.caption,
                    operation,
                )
            )

        return cur, cap

    # =============================================================
    # VELOCIDAD
    # =============================================================

    def animation_time(
        self,
        text,
        operation,
    ):

        text = text.lower()

        if operation == "delete":

            if any(
                x in text
                for x in (
                    "merge",
                    "fusion",
                    "prestamo",
                    "préstamo",
                    "sube",
                    "baja",
                    "predecesor",
                    "sucesor",
                    "propagar",
                    "raíz",
                )
            ):
                return 1.15

            return 0.72

        if operation == "insert":

            if any(
                x in text
                for x in (
                    "split",
                    "sube",
                    "promov",
                )
            ):
                return 0.9

            return 0.6

        return 0.6

    # =============================================================
    # PAUSAS
    # =============================================================

    def pause_time(
        self,
        text,
        operation,
    ):

        text = text.lower()

        if operation == "delete":

            if any(
                x in text
                for x in (
                    "merge",
                    "fusion",
                )
            ):
                return 1.45

            if any(
                x in text
                for x in (
                    "prestamo",
                    "préstamo",
                    "sube",
                    "baja",
                    "propagar",
                    "raíz",
                    "encontramos",
                )
            ):
                return 1.2

            return 0.72

        if operation == "insert":

            if any(
                x in text
                for x in (
                    "split",
                    "sube",
                    "promov",
                )
            ):
                return 1.05

            return 0.48

        return 0.8

    # =============================================================
    # TEXTO SUPERIOR
    # =============================================================

    def keys_label(
        self,
        keys,
        prefix,
        color,
    ):

        text = Text(
            f"{prefix} "
            + ", ".join(
                str(k)
                for k in keys
            ),
            font_size=22,
            color=color,
        )

        return text.to_corner(
            UL,
            buff=0.5,
        ).shift(
            DOWN * 0.8,
        )
