# Algoritmo B-Tree puro.
# Genera pasos pedagógicos explícitos para animar inserción,
# eliminación y búsqueda.

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class Node:
    keys: List[int] = field(default_factory=list)
    children: List["Node"] = field(default_factory=list)
    leaf: bool = True

    def clone(self) -> "Node":
        n = Node(leaf=self.leaf)
        n.keys = list(self.keys)
        n.children = [c.clone() for c in self.children]
        return n


@dataclass
class Step:
    tree: Node
    highlight_path: List[int]
    caption: str
    inserted_key: Optional[int] = None


class BTree:
    def __init__(self, degree: int = 3):
        self.degree = degree
        self.max_keys = degree - 1
        self.root = Node(leaf=True)

    # =============================================================
    # UTILIDADES
    # =============================================================

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

    def _min_keys(self) -> int:
        # Para m=3 -> mínimo 1 clave en nodos no raíz.
        return (self.degree + 1) // 2 - 1

    def _add_step(
        self,
        steps: Optional[List[Step]],
        caption: str,
        highlight_path=None,
        inserted_key=None,
    ):
        if steps is not None:
            steps.append(
                Step(
                    self.root.clone(),
                    list(highlight_path or []),
                    caption,
                    inserted_key=inserted_key,
                )
            )

    # =============================================================
    # INSERCIÓN
    # =============================================================

    def insert_silent(self, key: int):
        self._insert(key, steps=None)

    def insert_with_steps(self, key: int) -> List[Step]:
        steps: List[Step] = []
        self._insert(key, steps=steps)
        return steps

    def _insert(self, key: int, steps: Optional[List[Step]]):
        if self._contains(self.root, key):
            self._add_step(
                steps,
                f"{key} ya existe.",
            )
            return

        self._add_step(
            steps,
            f"Queremos insertar {key}.",
        )

        node = self.root
        path = []

        while not node.leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            self._add_step(
                steps,
                f"Comparamos {key} y bajamos por el hijo {i}.",
                [idx for _, idx in path] + [i],
            )

            path.append((node, i))
            node = node.children[i]

        pos = 0
        while pos < len(node.keys) and key > node.keys[pos]:
            pos += 1

        self._add_step(
            steps,
            f"Encontramos la hoja. Colocamos {key} en su posición.",
            [idx for _, idx in path],
        )

        node.keys.insert(pos, key)

        self._add_step(
            steps,
            f"{key} fue insertado. Verificamos si el nodo excede el máximo.",
            [idx for _, idx in path],
            inserted_key=key,
        )

        self._split_up(path, steps)

        self._add_step(
            steps,
            f"Inserción de {key} terminada.",
        )

    def _split_up(self, path, steps):
        path = list(path)

        if path:
            parent, idx = path[-1]
            current = parent.children[idx]
        else:
            parent, idx = None, 0
            current = self.root

        while len(current.keys) > self.max_keys:
            mid = len(current.keys) // 2
            median = current.keys[mid]

            self._add_step(
                steps,
                f"El nodo tiene {len(current.keys)} claves: hacemos split.",
                [i for _, i in path],
            )

            self._add_step(
                steps,
                f"Tomamos {median} como clave central. Será promovida.",
                [i for _, i in path],
            )

            left = Node(leaf=current.leaf)
            right = Node(leaf=current.leaf)

            left.keys = current.keys[:mid]
            right.keys = current.keys[mid + 1:]

            if not current.leaf:
                left.children = current.children[:mid + 1]
                right.children = current.children[mid + 1:]

            if parent is None:
                new_root = Node(leaf=False)
                new_root.keys = [median]
                new_root.children = [left, right]
                self.root = new_root

                self._add_step(
                    steps,
                    f"{median} sube y se convierte en la nueva raíz.",
                )

                return

            parent_highlight = [i for _, i in path[:-1]]

            # Estado después de preparar los dos nodos.
            parent.children[idx] = left
            parent.children.insert(idx + 1, right)

            self._add_step(
                steps,
                f"Dividimos el nodo alrededor de {median}.",
                parent_highlight,
            )

            parent.keys.insert(idx, median)

            self._add_step(
                steps,
                f"{median} sube al padre.",
                parent_highlight,
            )

            current = parent

            if path:
                path.pop()

            if path:
                parent, idx = path[-1]
            else:
                parent, idx = None, 0

    # =============================================================
    # BÚSQUEDA
    # =============================================================

    def search_with_steps(self, key: int) -> List[Step]:
        steps = [
            Step(
                self.root.clone(),
                [],
                f"Comenzamos a buscar {key}.",
            )
        ]

        node = self.root
        path = []

        while True:
            i = 0

            self._add_step(
                steps,
                f"Buscamos {key} dentro del nodo actual.",
                path,
            )

            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            if i < len(node.keys) and node.keys[i] == key:
                self._add_step(
                    steps,
                    f"Encontrado: {key}.",
                    path,
                )
                return steps

            if node.leaf:
                self._add_step(
                    steps,
                    f"{key} no está en el árbol.",
                    path,
                )
                return steps

            self._add_step(
                steps,
                f"{key} no está aquí. Bajamos por el hijo {i}.",
                path + [i],
            )

            path.append(i)
            node = node.children[i]

    # =============================================================
    # ELIMINACIÓN
    # =============================================================

    def delete_with_steps(self, key: int) -> List[Step]:
        steps: List[Step] = []

        if not self._contains(self.root, key):
            self._add_step(
                steps,
                f"{key} no está en el árbol.",
            )
            return steps

        self._add_step(
            steps,
            f"Comenzamos a buscar {key} para eliminarla.",
        )

        self._delete(
            self.root,
            key,
            steps,
            [],
        )

        # La raíz puede quedar vacía después de un merge.
        if not self.root.leaf and len(self.root.keys) == 0:
            self._add_step(
                steps,
                "La raíz quedó sin claves. Verificamos sus hijos.",
            )

            self.root = self.root.children[0]

            self._add_step(
                steps,
                "El único hijo sube y se convierte en la nueva raíz.",
            )

        self._add_step(
            steps,
            f"Eliminación de {key} terminada.",
        )

        return steps

    def _delete(
        self,
        node: Node,
        key: int,
        steps: List[Step],
        route: List[int],
    ):
        idx = 0

        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1

        # ---------------------------------------------------------
        # ENCONTRAMOS LA CLAVE
        # ---------------------------------------------------------

        if idx < len(node.keys) and node.keys[idx] == key:

            self._add_step(
                steps,
                f"Encontramos {key} en este nodo.",
                route,
            )

            # -----------------------------------------------------
            # CASO 1: HOJA
            # -----------------------------------------------------

            if node.leaf:
                self._add_step(
                    steps,
                    f"{key} está en una hoja. La eliminamos.",
                    route,
                )

                node.keys.pop(idx)

                self._add_step(
                    steps,
                    f"{key} fue eliminada. Ahora verificamos el nodo.",
                    route,
                )

                return

            # -----------------------------------------------------
            # CASO 2: NODO INTERNO
            # -----------------------------------------------------

            self._add_step(
                steps,
                f"{key} está en un nodo interno. Primero revisamos sus hijos.",
                route,
            )

            self._delete_internal(
                node,
                idx,
                steps,
                route,
            )

            return

        # ---------------------------------------------------------
        # NO ESTÁ EN ESTE NODO
        # ---------------------------------------------------------

        if node.leaf:
            return

        child_idx = idx

        self._add_step(
            steps,
            f"{key} no está en este nodo. Debemos bajar por el hijo {child_idx}.",
            route + [child_idx],
        )

        min_k = self._min_keys()
        child = node.children[child_idx]

        self._add_step(
            steps,
            f"Antes de bajar, verificamos cuántas claves tiene el hijo: {len(child.keys)}.",
            route + [child_idx],
        )

        if len(child.keys) <= min_k:
            self._add_step(
                steps,
                "El hijo está en el mínimo permitido. Debemos asegurarnos de que no quede vacío.",
                route + [child_idx],
            )

            child_idx = self._fill(
                node,
                child_idx,
                steps,
                route,
            )

        self._delete(
            node.children[child_idx],
            key,
            steps,
            route + [child_idx],
        )

    # =============================================================
    # ELIMINAR DESDE NODO INTERNO
    # =============================================================

    def _delete_internal(
        self,
        node: Node,
        idx: int,
        steps,
        route,
    ):
        key = node.keys[idx]
        left = node.children[idx]
        right = node.children[idx + 1]
        min_k = self._min_keys()

        self._add_step(
            steps,
            f"Los hijos de {key} son el izquierdo y el derecho.",
            route,
        )

        self._add_step(
            steps,
            f"Hijo izquierdo: {left.keys}. Hijo derecho: {right.keys}.",
            route,
        )

        # ---------------------------------------------------------
        # CASO A: IZQUIERDO PUEDE PRESTAR
        # ---------------------------------------------------------

        if len(left.keys) > min_k:

            pred = self._get_max(left)

            self._add_step(
                steps,
                f"El hijo izquierdo tiene más del mínimo. Usaremos su predecesor {pred}.",
                route + [idx],
            )

            node.keys[idx] = pred

            self._add_step(
                steps,
                f"Subimos/reemplazamos {key} por su predecesor {pred}.",
                route,
            )

            self._delete(
                left,
                pred,
                steps,
                route + [idx],
            )

            return

        # ---------------------------------------------------------
        # CASO B: DERECHO PUEDE PRESTAR
        # ---------------------------------------------------------

        if len(right.keys) > min_k:

            succ = self._get_min(right)

            self._add_step(
                steps,
                f"El izquierdo está en el mínimo. El derecho puede aportar. Usaremos {succ}.",
                route + [idx + 1],
            )

            node.keys[idx] = succ

            self._add_step(
                steps,
                f"Reemplazamos {key} por su sucesor {succ}.",
                route,
            )

            self._delete(
                right,
                succ,
                steps,
                route + [idx + 1],
            )

            return

        # ---------------------------------------------------------
        # CASO C: AMBOS ESTÁN EN EL MÍNIMO
        # ---------------------------------------------------------

        self._add_step(
            steps,
            f"Ambos hijos tienen el mínimo ({min_k}). No podemos pedir prestado.",
            route,
        )

        self._add_step(
            steps,
            f"Debemos fusionar: hijo izquierdo + {key} + hijo derecho.",
            route,
        )

        self._merge(
            node,
            idx,
            steps,
            route,
        )

        merged_path = route + [idx]

        self._add_step(
            steps,
            f"Después del merge, continuamos buscando {key} dentro del nodo fusionado.",
            merged_path,
        )

        self._delete(
            node.children[idx],
            key,
            steps,
            merged_path,
        )

    # =============================================================
    # REPARAR HIJO ANTES DE BAJAR
    # =============================================================

    def _fill(
        self,
        node: Node,
        idx: int,
        steps,
        route,
    ) -> int:

        min_k = self._min_keys()

        child = node.children[idx]

        # ---------------------------------------------------------
        # HERMANO IZQUIERDO
        # ---------------------------------------------------------

        if (
            idx > 0
            and len(node.children[idx - 1].keys) > min_k
        ):
            self._add_step(
                steps,
                "El hermano izquierdo tiene una clave extra. Podemos pedir prestado.",
                route + [idx],
            )

            self._borrow_left(
                node,
                idx,
            )

            self._add_step(
                steps,
                f"Préstamo desde la izquierda. La clave del padre baja al hijo y otra sube.",
                route,
            )

            return idx

        # ---------------------------------------------------------
        # HERMANO DERECHO
        # ---------------------------------------------------------

        if (
            idx < len(node.keys)
            and len(node.children[idx + 1].keys) > min_k
        ):
            self._add_step(
                steps,
                "El hermano derecho tiene una clave extra. Podemos pedir prestado.",
                route + [idx],
            )

            self._borrow_right(
                node,
                idx,
            )

            self._add_step(
                steps,
                "Préstamo desde la derecha. La clave del padre baja al hijo y otra sube.",
                route,
            )

            return idx

        # ---------------------------------------------------------
        # MERGE CON IZQUIERDA
        # ---------------------------------------------------------

        if idx > 0:

            self._add_step(
                steps,
                "Ningún hermano puede prestar. Fusionamos con el hermano izquierdo.",
                route,
            )

            self._merge(
                node,
                idx - 1,
                steps,
                route,
            )

            return idx - 1

        # ---------------------------------------------------------
        # MERGE CON DERECHA
        # ---------------------------------------------------------

        self._add_step(
            steps,
            "Ningún hermano puede prestar. Fusionamos con el hermano derecho.",
            route,
        )

        self._merge(
            node,
            idx,
            steps,
            route,
        )

        return idx

    # =============================================================
    # PRÉSTAMOS
    # =============================================================

    def _borrow_left(self, node, idx):

        child = node.children[idx]
        left = node.children[idx - 1]

        # Primero baja la clave del padre.
        child.keys.insert(
            0,
            node.keys[idx - 1],
        )

        # Luego sube la mayor del hermano.
        node.keys[idx - 1] = left.keys.pop()

        if not left.leaf:
            child.children.insert(
                0,
                left.children.pop(),
            )

    def _borrow_right(self, node, idx):

        child = node.children[idx]
        right = node.children[idx + 1]

        # Primero baja la clave del padre.
        child.keys.append(
            node.keys[idx],
        )

        # Luego sube la menor del hermano.
        node.keys[idx] = right.keys.pop(0)

        if not right.leaf:
            child.children.append(
                right.children.pop(0),
            )

    # =============================================================
    # MERGE
    # =============================================================

    def _merge(
        self,
        node,
        idx,
        steps=None,
        route=None,
    ):
        route = list(route or [])

        left = node.children[idx]
        right = node.children[idx + 1]
        down_key = node.keys[idx]

        # ---------------------------------------------------------
        # PASO 1: IDENTIFICAR LOS ELEMENTOS
        # ---------------------------------------------------------

        if steps is not None:
            steps.append(
                Step(
                    self.root.clone(),
                    route,
                    f"Merge 1/5: seleccionamos [{left.keys}] + {down_key} + [{right.keys}].",
                )
            )

        # ---------------------------------------------------------
        # PASO 2: LA CLAVE DEL PADRE BAJA
        # ---------------------------------------------------------

        left.keys.append(down_key)

        if steps is not None:
            steps.append(
                Step(
                    self.root.clone(),
                    route + [idx],
                    f"Merge 2/5: {down_key} baja del padre al nodo izquierdo.",
                )
            )

        # ---------------------------------------------------------
        # PASO 3: UNIR LAS CLAVES
        # ---------------------------------------------------------

        if steps is not None:
            steps.append(
                Step(
                    self.root.clone(),
                    route + [idx],
                    f"Merge 3/5: unimos las claves del hermano derecho {right.keys}.",
                )
            )

        left.keys.extend(right.keys)

        # ---------------------------------------------------------
        # PASO 4: UNIR HIJOS Y ACTUALIZAR EL PADRE
        # ---------------------------------------------------------

        if not left.leaf:
            left.children.extend(right.children)

        # El padre deja de apuntar al hermano derecho.
        # Hacemos ambas operaciones juntas para no dibujar
        # temporalmente el mismo subárbol dos veces.
        node.keys.pop(idx)
        node.children.pop(idx + 1)

        if steps is not None:
            steps.append(
                Step(
                    self.root.clone(),
                    route + [idx],
                    "Merge 4/5: los hijos quedan unidos en el nodo izquierdo.",
                )
            )

        # ---------------------------------------------------------
        # PASO 5: RESULTADO DEL MERGE
        # ---------------------------------------------------------

        if steps is not None:
            steps.append(
                Step(
                    self.root.clone(),
                    route,
                    f"Merge 5/5: merge terminado. Resultado: {left.keys}.",
                )
            )

        # Si el padre queda vacío, eso se procesa arriba.
        if steps is not None and len(node.keys) == 0:
            steps.append(
                Step(
                    self.root.clone(),
                    route,
                    "El padre quedó sin claves. Debemos propagar la corrección hacia arriba.",
                )
            )

    # =============================================================
    # EXTREMOS
    # =============================================================

    def _get_max(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _get_min(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]


# ================================================================
# VALIDACIÓN
# ================================================================

def validar(root: Node, degree: int) -> Tuple[bool, str]:
    max_keys = degree - 1
    min_keys = (degree + 1) // 2 - 1

    def _profundidad(n):
        if n.leaf:
            return 0
        return 1 + _profundidad(n.children[0])

    def _check(n, es_raiz, prof_esperada, prof_actual):

        if any(
            n.keys[i] >= n.keys[i + 1]
            for i in range(len(n.keys) - 1)
        ):
            return False, f"Claves no ordenadas: {n.keys}"

        if not es_raiz and len(n.keys) < min_keys:
            return False, (
                f"Nodo con {len(n.keys)} claves "
                f"(min {min_keys}): {n.keys}"
            )

        if len(n.keys) > max_keys:
            return False, (
                f"Nodo con {len(n.keys)} claves "
                f"(max {max_keys}): {n.keys}"
            )

        if not n.leaf:

            if len(n.children) != len(n.keys) + 1:
                return False, (
                    f"{len(n.keys)} claves pero "
                    f"{len(n.children)} hijos"
                )

            for c in n.children:
                ok, msg = _check(
                    c,
                    False,
                    prof_esperada,
                    prof_actual + 1,
                )

                if not ok:
                    return False, msg

        else:

            if prof_actual != prof_esperada:
                return False, (
                    f"Hoja a profundidad {prof_actual}, "
                    f"esperada {prof_esperada}"
                )

        return True, "ok"

    prof = _profundidad(root)

    return _check(
        root,
        True,
        prof,
        0,
    )
