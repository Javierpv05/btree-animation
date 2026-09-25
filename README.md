# B-Trees animados con Manim

**Proyecto 1 — CS2023 Algoritmos y Estructuras de Datos**
Autores: Javier ,Ernesto 2, Integrante 3
Septiembre 2026

## Descripción

Animación educativa de un **B-Tree** usando [Manim Community](https://www.manim.community/).
Cubre: motivación (problema del BST), definición, propiedades,
ventajas frente a estructuras binarias, ejemplo, inserción, split,
eliminación y aplicaciones.

## Requisitos

- Python 3.9+
- FFmpeg
- Cairo, Pango

### Arch Linux

```bash
sudo pacman -S python python-pip ffmpeg cairo pango pkgconf
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cómo ejecutar

```bash
# Escena individual (rápido, para probar)
manim -pql scenes/btree_insert.py BTreeInsert

# Render final y video unido
./render.sh
```

## Estructura

```
scenes/   -> cada escena del video
utils/    -> algoritmo B-Tree puro + helpers de layout
```

## Referencias

- Cormen et al., *Introduction to Algorithms*, cap. 18.
- Bayer & McCreight (1972).
- Manim Community: <https://docs.manim.community/>