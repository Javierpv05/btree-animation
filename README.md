<h1 align="center"> B-Trees Animados con Manim</h1>

<p align="center">
  <b>Proyecto 1 </b><br>
  Animación educativa del algoritmo <b>B-Tree</b> usando <a href="https://www.manim.community/">Manim Community</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white">
  <img alt="Manim" src="https://img.shields.io/badge/Manim-0.18%2B-green?logo=manim&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-Académica-lightgrey">
</p>

---

## Integrantes:

- Victor Paolo Soto Ruiz
- 
-

---

## ¿Que es este proyecto ? 

Una animación educativa que explica el **B-Tree** paso a paso:
- Por qué existe (y qué problema resuelve frente a un BST).
- Sus propiedades y reglas con grado `m`.
- Cómo funciona la **inserción**, **eliminación**, **split** y **búsqueda**.
- Dónde se usa en el mundo real (bases de datos, filesystems, etc.).

El video final dura **~3 minutos** y está renderizado en **1080p60**.

---

## 📂 Estructura del proyecto

```
btree-animation/
│
├── 📁 scenes/              # Cada escena del video (una por archivo)
│   ├── intro.py
│   ├── bst_intro.py
│   ├── problema_bst.py
│   ├── btree_intro.py
│   ├── btree_propiedades.py
│   ├── btree_split.py
│   ├── btree_ejemplo.py
│   ├── btree_aplicaciones.py
│   └── outro.py
│
├── 📁 utils/               # Código reutilizable
│   ├── btree.py            # algoritmo b-tree
│   └── btree_layout.py     # Constantes de layout + helpers gráficos
│
├── 📄 render.sh            # Script que renderiza TODO y une en video_final.mp4
├── 📄 test_btree.py        # Tests del algoritmo (validan invariantes)
├── 📄 requirements.txt     # Dependencias de Python
├── 📄 .gitignore
└── 📄 README.md
```

### ¿Qué hay en cada carpeta?

| Carpeta | Qué contiene | Para qué sirve |
|---|---|---|
| `scenes/` | Una escena de Manim por archivo | Cada archivo es una pieza narrativa del video |
| `utils/btree.py` | Algoritmo B-Tree puro | Genera los pasos que las escenas animan |
| `utils/btree_layout.py` | Helpers gráficos | Nodos, títulos, captions, tablas, rutas resaltadas |
| `media/` | Salida de Manim *(auto-generada)* | Aquí caen los `.mp4` de cada escena |

---

##  Requisitos del sistema

| Requisito | Versión mínima | Para qué |
|---|---|---|
| Python | 3.9+ | Correr Manim y el algoritmo |
| FFmpeg | 4.0+ | Renderizar y unir videos |
| Cairo + Pango | — | Dependencias nativas de Manim |

### Instalación en Arch Linux

```bash
sudo pacman -S python python-pip ffmpeg cairo pango pkgconf
```

### Otras distros

- **Debian/Ubuntu:** `sudo apt install python3 python3-pip ffmpeg libcairo2-dev libpango1.0-dev`
- **macOS (Homebrew):** `brew install python ffmpeg cairo pango pkg-config`
- **Windows:** ver la [guía oficial de Manim](https://docs.manim.community/en/stable/installation/windows.html)

---

## Ejecucion del proyecto 

### 1. Clonar el repositorio

```bash
git clone https://github.com/Javierpv05/btree-animation.git
cd btree-animation
```

### 2. Crear el entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate       # Windows
```

> Sabrás que está activo porque tu prompt cambia a `(.venv) ...`.

### 3. Instalar las dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Debe terminar con: **`✅ Todos los tests pasaron.`**

---

## Cómo renderizar el video

### Probar una escena individual (rápido)

Útil mientras desarrollas. Tarda ~5 segundos por escena.

```bash
manim -pql scenes/intro.py Intro
```

Flags útiles:
- `-p` → reproduce el video al terminar
- `-q` + `l` → **l**ow quality (480p, rápido)
- `-q` + `h` → **h**igh quality (1080p, lento, para render final)

### Renderizar TODO el video

Cuando todas las escenas se vean bien:

```bash
./render.sh
```

Esto:
1. Renderiza cada escena a **1080p60** (~15 min en total).
2. Une todos los `.mp4` en **`video_final.mp4`**.

### Convertir a MPEG (si lo pide el profe)

```bash
ffmpeg -i video_final.mp4 -c:v mpeg2video -qscale:v 2 -c:a mp2 video_final.mpg
```


## Tests del algoritmo

El archivo `test_btree.py` valida que el algoritmo respeta los invariantes del B-Tree:
- Claves ordenadas en cada nodo.
- Cantidad de claves dentro del rango `[⌈m/2⌉ − 1, m − 1]`.
- Cantidad de hijos = cantidad de claves + 1.
- Todas las hojas a la misma profundidad.

```bash
python test_btree.py
```

---

## Estructura 

| # | Escena | Qué muestra |
|---|---|---|
| 1 | `intro` | Título, autores, curso |
| 2 | `bst_intro` | Qué es un BST (versión corta) |
| 3 | `problema_bst` | Por qué un BST se degenera + tabla |
| 4 | `btree_intro` | Qué es un B-Tree + comparación con BST |
| 5 | `btree_propiedades` | Grado `m`, reglas con `⌈m/2⌉`, complejidades |
| 6 | `btree_split` | Split (inserción) y merge (eliminación) |
| 7 | `btree_ejemplo` | Ejemplo completo: insert + delete + search |
| 8 | `btree_aplicaciones` | RAM vs disco + aplicaciones reales |
| 9 | `outro` | Cierre |

---

##  Autores

| Integrante |
|---|
| Javier Pariansullca Ventura |
| Ernesto Sullca Toledo |
| Paolo Ruiz Soto |

**Curso:** Algoritmos y Estructuras de Datos  
**Fecha:** Septiembre 2026

---

##  Referencias

- Cormen, Leiserson, Rivest, Stein. *Introduction to Algorithms*, 4ª ed., Capítulo 18.
- Bayer, R., McCreight, E. (1972). *Organization and Maintenance of Large Ordered Indices*.
- [Manim Community — Documentación oficial](https://docs.manim.community/)
- [3Blue1Brown](https://www.3blue1brown.com/) — inspiración visual

---

<p align="center"><i>Hecho con 🐍 Python y 🎬 Manim</i></p>