"""
Constantes de layout y helpers reutilizables para las escenas.
"""
from manim import *


# ============================================================
# ZONAS VERTICALES
# ============================================================
Y_TITULO        =  3.4
Y_SUBTITULO     =  2.7
Y_CONTENIDO_TOP =  2.0
Y_CONTENIDO_BOT = -1.8
Y_CAPTION       = -3.2

NIVEL_Y = {0: 2.0, 1: 0.2, 2: -1.6}
COL_X   = [-4.5, -1.5, 1.5, 4.5]
COL_X_2 = [-2.5, 2.5]

KEY_W = 0.75
KEY_H = 0.65

FS_TITULO    = 44
FS_SUBTITULO = 24
FS_TEXTO     = 24
FS_CAPTION   = 22
FS_CLAVE     = 22
FS_ETIQUETA  = 18


# ============================================================
# HELPERS BÁSICOS
# ============================================================
def make_node(keys, color=GREEN):
    cajas = VGroup(*[
        Rectangle(width=KEY_W, height=KEY_H, color=color, stroke_width=2)
        for _ in keys
    ]).arrange(RIGHT, buff=0)
    textos = VGroup(*[
        Text(str(k), font_size=FS_CLAVE).move_to(c)
        for k, c in zip(keys, cajas)
    ])
    return VGroup(cajas, textos)


def connect(parent, child, color=GREEN):
    return Line(parent.get_bottom(), child.get_top(), color=color, stroke_width=2)


def caption(text, color=YELLOW):
    return Text(text, font_size=FS_CAPTION, color=color).move_to([0, Y_CAPTION, 0])


def titulo(text, color=GREEN):
    return Text(text, font_size=FS_TITULO, color=color).move_to([0, Y_TITULO, 0])


def highlight(node, color=YELLOW, opacity=0.3):
    return node[0].animate.set_color(color).set_fill(color, opacity=opacity)


def unhighlight(node, color=GREEN):
    return node[0].animate.set_color(color).set_fill(color, opacity=0)


# ============================================================
# REEMPLAZO DE CAPTIONS SIN SUPERPONER
# ============================================================
def switch_caption(old_cap, new_cap):
    """Crossfade limpio entre captions (nunca usar Transform en textos)."""
    return [
        FadeOut(old_cap, shift=UP * 0.15),
        FadeIn(new_cap, shift=DOWN * 0.15),
    ]


# ============================================================
# TABLAS ALINEADAS
# ============================================================
def tabla_columnas(columnas_x, headers, filas,
                   y_header=1.2, y_inicio=0.6, dy=0.6,
                   fs_header=22, fs_fila=20,
                   color_header=YELLOW,
                   colores_fila=None):
    """Construye tabla con columnas alineadas (x fijo por columna)."""
    header_group = VGroup()
    for x, txt in zip(columnas_x, headers):
        header_group.add(
            Text(txt, font_size=fs_header, color=color_header).move_to([x, y_header, 0])
        )

    filas_group = VGroup()
    for i, fila in enumerate(filas):
        y = y_inicio - i * dy
        for j, txt in enumerate(fila):
            if colores_fila is not None:
                color = colores_fila(i, j)
            elif j == 0:
                color = WHITE
            else:
                color = BLUE if j % 2 == 1 else GREEN
            filas_group.add(
                Text(txt, font_size=fs_fila, color=color).move_to([columnas_x[j], y, 0])
            )

    return header_group, filas_group


def linea_tabla(y, ancho=7, color=GREY):
    return Line([-ancho, y, 0], [ancho, y, 0], color=color, stroke_width=2)


# ============================================================
# CONVERSIÓN Node -> VGroup
# ============================================================
from utils.btree import Node  # noqa: E402


def compute_positions(root: Node, x_spacing=1.9, y_spacing=1.4, y_top=2.2):
    """Asigna (x, y) a cada nodo. Hojas de izq a der; internos centrados."""
    positions = {}
    leaf_counter = [0]

    def dfs(node, depth):
        if node.leaf:
            x = leaf_counter[0]
            leaf_counter[0] += 1
        else:
            for c in node.children:
                dfs(c, depth + 1)
            xs = [positions[id(c)][0] for c in node.children]
            x = sum(xs) / len(xs)
        positions[id(node)] = (x, depth)

    dfs(root, 0)

    xs_all = [p[0] for p in positions.values()]
    center_x = (min(xs_all) + max(xs_all)) / 2

    result = {}
    for nid, (x, d) in positions.items():
        result[nid] = ((x - center_x) * x_spacing, y_top - d * y_spacing)
    return result


def tree_to_vgroup(
    root: Node,
    highlight_path=None,
    normal_color=GREEN,
    path_color=YELLOW,
    target_color=ORANGE,
    path_edge_color=YELLOW,
    path_edge_width=5,
    normal_edge_width=2,
    path_stroke_width=4,
):
    """
    Convierte un árbol en un VGroup marcando la RUTA.
    Las líneas salen de las esquinas reales de las cajas del padre
    calculando posiciones con matemáticas directas (KEY_W, KEY_H).
    """
    if highlight_path is None:
        highlight_path = []
        sin_resaltado = True
    else:
        sin_resaltado = False

    positions = compute_positions(root)

    if sin_resaltado:
        path_set = set()
        target_id = None
    else:
        path_ids = [id(root)]
        cursor = root
        for idx in highlight_path:
            if idx < len(cursor.children):
                cursor = cursor.children[idx]
                path_ids.append(id(cursor))
        target_id = path_ids[-1]
        path_set = set(path_ids)

    path_edges = set()
    if not sin_resaltado:
        cursor = root
        for idx in highlight_path:
            if idx < len(cursor.children):
                path_edges.add((id(cursor), idx))
                cursor = cursor.children[idx]

    node_mobs = {}

    def build(node):
        x, y = positions[id(node)]

        if target_id is not None and id(node) == target_id:
            mob = make_node(node.keys, color=target_color)
            mob[0].set_stroke(width=path_stroke_width)
            mob[0].set_fill(target_color, opacity=0.25)
        elif id(node) in path_set:
            mob = make_node(node.keys, color=path_color)
            mob[0].set_stroke(width=path_stroke_width)
        else:
            mob = make_node(node.keys, color=normal_color)

        node_mobs[id(node)] = mob.move_to([x, y, 0])
        for child in node.children:
            build(child)

    build(root)

    lines = VGroup()

    def _start_points(node):
        """
        Calcula los puntos de salida de las líneas con matemáticas
        directas (sin get_corner) para evitar errores con sub-grupos.

        Para un nodo con k claves hay k+1 vértices en la base:
            - vértice 0: borde inferior izquierdo
            - vértice i (1..k-1): unión entre clave i-1 y clave i
            - vértice k: borde inferior derecho
        """
        n_keys = len(node.keys)
        n_hijos = len(node.children)
        x_center, y_center = positions[id(node)]

        if n_keys == 0:
            # Nodo vacío: usar el centro inferior como fallback
            y_bottom = y_center - KEY_H / 2
            return [[x_center, y_bottom, 0]] * n_hijos

        # Base del nodo (centro menos media altura)
        y_bottom = y_center - KEY_H / 2

        # El grupo de cajas tiene ancho total = n_keys * KEY_W
        # Su borde izquierdo está en x_center - ancho_total/2
        x_left = x_center - (n_keys * KEY_W) / 2

        # Vértices: izquierda, uniones intermedias, derecha
        return [
            [x_left + i * KEY_W, y_bottom, 0]
            for i in range(n_hijos)
        ]

    def add_lines(node):
        starts = _start_points(node)
        for i, child in enumerate(node.children):
            on_path = (id(node), i) in path_edges
            # CAMBIO: Line en lugar de Arrow (evita punta fantasma)
            lines.add(Line(
                start=starts[i],
                end=node_mobs[id(child)].get_top(),
                color=path_edge_color if on_path else normal_color,
                stroke_width=path_edge_width if on_path else normal_edge_width,
            ))
            add_lines(child)

    add_lines(root)

    group = VGroup()
    for mob in node_mobs.values():
        group.add(mob)
    group.add(lines)
    return group