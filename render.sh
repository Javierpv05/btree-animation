#!/bin/bash
# Renderiza todas las escenas del proyecto y las une en video_final.mp4.
set -e

echo "==> Renderizando escenas..."

manim -qh scenes/intro.py               Intro
manim -qh scenes/bst_intro.py           BSTIntro
manim -qh scenes/problema_bst.py        ProblemaBST
manim -qh scenes/btree_intro.py         BTreeIntro
manim -qh scenes/btree_propiedades.py   BTreePropiedades
manim -qh scenes/btree_split.py         BTreeSplit
manim -qh scenes/btree_ejemplo.py       BTreeEjemplo
manim -qh scenes/btree_aplicaciones.py  BTreeAplicaciones
manim -qh scenes/outro.py               Outro

echo "==> Uniendo videos..."

cat > lista.txt <<EOF
file 'media/videos/intro/1080p60/Intro.mp4'
file 'media/videos/bst_intro/1080p60/BSTIntro.mp4'
file 'media/videos/problema_bst/1080p60/ProblemaBST.mp4'
file 'media/videos/btree_intro/1080p60/BTreeIntro.mp4'
file 'media/videos/btree_propiedades/1080p60/BTreePropiedades.mp4'
file 'media/videos/btree_split/1080p60/BTreeSplit.mp4'
file 'media/videos/btree_ejemplo/1080p60/BTreeEjemplo.mp4'
file 'media/videos/btree_aplicaciones/1080p60/BTreeAplicaciones.mp4'
file 'media/videos/outro/1080p60/Outro.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i lista.txt -c copy video_final.mp4
rm lista.txt

echo "==> Listo: video_final.mp4"