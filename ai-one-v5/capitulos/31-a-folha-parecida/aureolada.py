"""Fotos da mancha-aureolada, a doença fora do conjunto."""
from pathlib import Path

import numpy as np
from PIL import Image

from dados.camera import fotografa
from dados.desenho import desenha

DESTINO = Path("dados/aureolada")
DESTINO.mkdir(parents=True, exist_ok=True)
s = np.random.default_rng(31)
for n in range(1, 61):
    intensidade = s.uniform(0.6, 1.4)
    desenho = desenha(31_000 + n, "aureolada", intensidade)
    fundo = str(s.choice(["terra", "folhagem"]))
    foto, _, _, _ = fotografa(desenho, s, fundo,
                              angulo=s.uniform(-15, 15),
                              escala=s.uniform(0.85, 1.1),
                              desloc=s.uniform(-10, 10, 2),
                              luz=s.uniform(0.8, 1.15))
    Image.fromarray(foto).save(DESTINO / f"{n:02d}.jpg",
                               quality=90)
print(f"60 fotos em {DESTINO}")
