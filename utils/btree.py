"""
utils/btree.py
==============
Implementación pura del algoritmo B-Tree (sin Manim).

Convención usada en todo el proyecto:
    grado m = máximo de hijos por nodo.

Propiedades derivadas:
    - máximo de claves por nodo = m - 1
    - mínimo de claves por nodo = ⌈m/2⌉ - 1   (excepto la raíz)
    - mínimo de hijos por nodo  = ⌈m/2⌉        (excepto la raíz)

La clase BTree genera listas de Steps con snapshots del árbol para
que las escenas de Manim puedan animar cada paso del algoritmo.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ============================================================
# NODO
# ============================================================
@dataclass
class Node:
    """
    Nodo del B-Tree.

    Invariante: si un nodo tiene k claves y no es hoja, tiene k+1 hijos.
    """
    keys: List[int] = field(default_factory=list)
    children: List["Node"] = field(default_factory=list)
    leaf: bool = True

    def clone(self) -> "Node":
        """Copia profunda (para guardar snapshots inmutables)."""
        n = Node(leaf=self.leaf)
        n.keys = list(self.keys)
        n.children = [c.clone() for c in self.children]
        return n


# ============================================================
# STEP: snapshot de un momento del algoritmo
# ============================================================
@dataclass
class Step:
    """
    Un paso listo para animar.

    Campos:
        tree:           estado del árbol en este paso (copia).
        highlight_path: ruta desde la raíz hacia el nodo a resaltar.
                        [] = solo la raíz, [0] = hijo 0, [0,1] = nieto 1...
        caption:        texto explicativo del paso.
        inserted_key:   clave recién insertada (si aplica).
    """
    tree: Node
    highlight_path: List[int]
    caption: str
    inserted_key: Optional[int] = None


# ============================================================
# B-TREE
# ============================================================
class BTree:
    def __init__(self, degree: int = 3):
        self.degree = degree
        self.max_keys = degree - 1
        self.root = Node(leaf=True)

    # ==========================================================
    # BÚSQUEDA
    # ==========================================================
    def contains(self, key: int) -> bool:
        return self._contains(self.root, key)

    def _contains(self, node: Node, key: int) -> bool:
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == key:
            return True
        if node.leaf:
            return False
        return self._contains(node.children[i], key)

    # ==========================================================
    # INSERCIÓN
    # ==========================================================
    def insert_silent(self, key: int):
        """Inserta sin generar steps (para construir árboles iniciales)."""
        self._insert(key, steps=None)

    def insert_with_steps(self, key: int) -> List[Step]:
        """Inserta y devuelve la lista de steps para animar."""
        steps: List[Step] = []
        self._insert(key, steps=steps)
        return steps

    def search_with_steps(self, key: int) -> List[Step]:
        """Recorre el árbol buscando `key` y devuelve los steps del camino."""
        steps = [Step(self.root.clone(), [], f"Buscar {key}")]
        node = self.root
        path = []
        while True:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and node.keys[i] == key:
                steps.append(Step(self.root.clone(), list(path),
                                  f"Encontrado: {key}"))
                return steps
            if node.leaf:
                steps.append(Step(self.root.clone(), list(path),
                                  f"{key} no está en el árbol"))
                return steps
            path.append(i)
            steps.append(Step(self.root.clone(), list(path),
                              f"Bajar por el hijo {i}"))
            node = node.children[i]

    def _insert(self, key: int, steps: Optional[List[Step]]):
        # --- Caso: ya existe ---
        if self._contains(self.root, key):
            if steps is not None:
                steps.append(Step(self.root.clone(), [], f"{key} ya existe."))
            return

        if steps is not None:
            steps.append(Step(self.root.clone(), [], f"Insertar {key}"))

        # --- Descender hasta la hoja, guardando el camino ---
        node = self.root
        path = []   # lista de (padre, índice_del_hijo)
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            path.append((node, i))
            if steps is not None:
                steps.append(Step(
                    self.root.clone(),
                    [idx for _, idx in path],
                    f"Bajar por el hijo {i} ({key}).",
                ))
            node = node.children[i]

        # --- Insertar en la hoja respetando el orden ---
        pos = 0
        while pos < len(node.keys) and key > node.keys[pos]:
            pos += 1
        node.keys.insert(pos, key)

        if steps is not None:
            steps.append(Step(
                self.root.clone(),
                [idx for _, idx in path],
                f"Insertar {key} en la hoja.",
                inserted_key=key,
            ))

        # --- Propagar splits hacia arriba ---
        self._split_up(path, steps)

        if steps is not None:
            steps.append(Step(self.root.clone(), [], f"{key} insertado."))

    def _split_up(self, path, steps):
        """
        Sube desde la hoja dividiendo cualquier nodo que se desborde.
        La clave media sube al padre; si el padre también se desborda,
        el proceso continúa hacia arriba.
        """
        path = list(path)   # copia local para no mutar el caller

        if path:
            parent, idx = path[-1]
            current = parent.children[idx]
        else:
            parent, idx = None, 0
            current = self.root

        while len(current.keys) > self.max_keys:
            mid = len(current.keys) // 2
            median = current.keys[mid]

            # Construir los dos hermanos
            left = Node(leaf=current.leaf)
            right = Node(leaf=current.leaf)
            left.keys = current.keys[:mid]
            right.keys = current.keys[mid + 1:]
            if not current.leaf:
                left.children = current.children[:mid + 1]
                right.children = current.children[mid + 1:]

            # Ruta hacia el padre (para resaltarlo en la animación)
            parent_highlight = [i for _, i in path[:-1]]

            # --- Caso especial: era la raíz → nueva raíz ---
            if parent is None:
                new_root = Node(leaf=False)
                new_root.keys = [median]
                new_root.children = [left, right]
                self.root = new_root
                if steps is not None:
                    steps.append(Step(
                        self.root.clone(), [],
                        f"Split en la raíz: sube {median}.",
                    ))
                return

            # --- Caso normal: insertar la mediana en el padre ---
            parent.keys.insert(idx, median)
            parent.children[idx] = left
            parent.children.insert(idx + 1, right)

            if steps is not None:
                steps.append(Step(
                    self.root.clone(), parent_highlight,
                    f"Split: {median} sube al padre.",
                ))

            # Seguir subiendo si el padre también se desbordó
            current = parent
            if path:
                path.pop()
                if path:
                    parent, idx = path[-1]
                else:
                    parent, idx = None, 0
            else:
                parent, idx = None, 0

    # ==========================================================
    # ELIMINACIÓN
    # ==========================================================
    def delete_with_steps(self, key: int) -> List[Step]:
        """Elimina y devuelve la lista de steps para animar."""
        steps: List[Step] = []

        if not self._contains(self.root, key):
            steps.append(Step(self.root.clone(), [], f"{key} no está."))
            return steps

        steps.append(Step(self.root.clone(), [], f"Eliminar {key}"))
        self._delete(self.root, key, steps, [])

        # Si la raíz quedó vacía (tras un merge), su único hijo es la nueva raíz.
        if not self.root.leaf and len(self.root.keys) == 0:
            self.root = self.root.children[0]
            steps.append(Step(self.root.clone(), [], "La raíz baja un nivel."))

        steps.append(Step(self.root.clone(), [], f"{key} eliminado."))
        return steps

    def _min_keys(self) -> int:
        """⌈m/2⌉ - 1"""
        return (self.degree + 1) // 2 - 1

    def _delete(self, node: Node, key: int, steps, route):
        # 1. Localizar la posición de la clave
        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1

        # 2. La clave está en este nodo
        if idx < len(node.keys) and node.keys[idx] == key:
            if node.leaf:
                node.keys.pop(idx)
                steps.append(Step(
                    self.root.clone(), route,
                    f"Quitar {key} de la hoja.",
                ))
            else:
                self._delete_internal(node, idx, steps, route)
            return

        # 3. Es hoja y no está → no existe (ya validado antes)
        if node.leaf:
            return

        # 4. Antes de descender: asegurar que el hijo tenga suficientes claves
        min_k = self._min_keys()
        child_idx = idx   # puede cambiar tras _fill

        if len(node.children[idx].keys) <= min_k:
            child_idx = self._fill(node, idx, steps, route)

        # 5. Descender al hijo correcto
        if child_idx < len(node.children):
            self._delete(
                node.children[child_idx],
                key,
                steps,
                route + [child_idx],
            )

    def _delete_internal(self, node: Node, idx: int, steps, route):
        """La clave está en un nodo interno: usar predecesor, sucesor o merge."""
        key = node.keys[idx]
        left = node.children[idx]
        right = node.children[idx + 1]
        min_k = self._min_keys()

        if len(left.keys) > min_k:
            # Predecesor: máximo del subárbol izquierdo
            pred = self._get_max(left)
            node.keys[idx] = pred
            steps.append(Step(
                self.root.clone(), route,
                f"Reemplazar con predecesor {pred}.",
            ))
            self._delete(left, pred, steps, route + [idx])

        elif len(right.keys) > min_k:
            # Sucesor: mínimo del subárbol derecho
            succ = self._get_min(right)
            node.keys[idx] = succ
            steps.append(Step(
                self.root.clone(), route,
                f"Reemplazar con sucesor {succ}.",
            ))
            self._delete(right, succ, steps, route + [idx + 1])

        else:
            # Ningún hijo tiene suficientes claves → merge paso a paso
            self._merge(node, idx, steps, route)
            self._delete(left, key, steps, route + [idx])

    def _get_max(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _get_min(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def _fill(self, node: Node, idx: int, steps, route) -> int:
        """
        Garantiza que node.children[idx] tenga más de min_keys claves.
        Devuelve el índice actualizado del hijo por el que descender.
        """
        min_k = self._min_keys()

        # Préstamo del hermano izquierdo
        if idx > 0 and len(node.children[idx - 1].keys) > min_k:
            self._borrow_left(node, idx)
            steps.append(Step(
                self.root.clone(), route + [idx],
                f"Préstamo del hermano izquierdo → padre {node.keys}.",
            ))
            return idx

        # Préstamo del hermano derecho
        if idx < len(node.keys) and len(node.children[idx + 1].keys) > min_k:
            self._borrow_right(node, idx)
            steps.append(Step(
                self.root.clone(), route + [idx],
                f"Préstamo del hermano derecho → padre {node.keys}.",
            ))
            return idx

        # Merge con hermano izquierdo
        if idx > 0:
            self._merge(node, idx - 1, steps, route)
            return idx - 1

        # Merge con hermano derecho
        self._merge(node, idx, steps, route)
        return idx

    def _borrow_left(self, node, idx):
        """
        Rota una clave del hermano izquierdo a través del padre.
        El padre baja una clave al hijo y el hermano sube su mayor clave.
        """
        child = node.children[idx]
        left = node.children[idx - 1]
        child.keys.insert(0, node.keys[idx - 1])
        node.keys[idx - 1] = left.keys.pop()
        if not left.leaf:
            child.children.insert(0, left.children.pop())

    def _borrow_right(self, node, idx):
        """Simétrico al préstamo izquierdo."""
        child = node.children[idx]
        right = node.children[idx + 1]
        child.keys.append(node.keys[idx])
        node.keys[idx] = right.keys.pop(0)
        if not right.leaf:
            child.children.append(right.children.pop(0))

    def _merge(self, node, idx, steps=None, route=None):
        """
        Fusiona node.children[idx], la clave node.keys[idx] y
        node.children[idx+1] en un solo nodo (el de la izquierda).
        Genera 3 sub-pasos para que la animación sea detallada.
        """
        left = node.children[idx]
        right = node.children[idx + 1]
        down_key = node.keys[idx]

        if steps is not None:
            steps.append(Step(
                self.root.clone(), route if route else [],
                f"Merge (1/3): la clave {down_key} baja del padre.",
            ))

        # Bajar la clave del padre al hijo izquierdo
        left.keys.append(down_key)

        if steps is not None:
            steps.append(Step(
                self.root.clone(), (route + [idx]) if route else [idx],
                f"Merge (2/3): {down_key} se une al hijo izquierdo.",
            ))

        # Fusionar con el hermano derecho
        left.keys.extend(right.keys)
        left.children.extend(right.children)
        node.keys.pop(idx)
        node.children.pop(idx + 1)

        if steps is not None:
            steps.append(Step(
                self.root.clone(), route if route else [],
                f"Merge (3/3): nodos fusionados → {left.keys}.",
            ))


# ============================================================
# VALIDACIÓN DE INVARIANTES
# ============================================================
def validar(root: Node, degree: int) -> Tuple[bool, str]:
    """
    Verifica los invariantes del B-Tree.
    """
    max_keys = degree - 1
    min_keys = (degree + 1) // 2 - 1

    def _profundidad(n):
        if n.leaf:
            return 0
        return 1 + _profundidad(n.children[0])

    def _check(n, es_raiz, prof_esperada, prof_actual):
        if any(n.keys[i] >= n.keys[i + 1] for i in range(len(n.keys) - 1)):
            return False, f"Claves no ordenadas: {n.keys}"

        if not es_raiz and len(n.keys) < min_keys:
            return False, f"Nodo con {len(n.keys)} claves (min {min_keys}): {n.keys}"
        if len(n.keys) > max_keys:
            return False, f"Nodo con {len(n.keys)} claves (max {max_keys}): {n.keys}"

        if not n.leaf:
            if len(n.children) != len(n.keys) + 1:
                return False, f"{len(n.keys)} claves pero {len(n.children)} hijos"
            for c in n.children:
                ok, msg = _check(c, False, prof_esperada, prof_actual + 1)
                if not ok:
                    return False, msg
        else:
            if prof_actual != prof_esperada:
                return False, f"Hoja a profundidad {prof_actual}, esperada {prof_esperada}"
        return True, "ok"

    prof = _profundidad(root)
    return _check(root, True, prof, 0)