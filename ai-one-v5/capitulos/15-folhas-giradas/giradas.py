"""As mesmas folhas fotografadas em pé e em qualquer ângulo."""
import csv
from pathlib import Path

import numpy as np
from PIL import Image

from dados.camera import fotografa
from dados.desenho import desenha
from dados.gerar_conjunto import FOLHAS

DESTINO = Path("dados/giradas")
s = np.random.default_rng(15)
classes = [c for c, n in FOLHAS.items() for _ in range(n // 5)]
linhas = []
for pasta in ("em_pe", "girada"):
    (DESTINO / pasta).mkdir(parents=True, exist_ok=True)
for n, verdade in enumerate(classes, 1):
    desenho = desenha(15_000 + n, verdade, s.uniform(0.4, 1.4))
    lab = s.random() < (0.8 if verdade == "ferrugem" else 0.08)
    fundo = "mesa"
    if not lab:
        fundo = str(s.choice(["terra", "folhagem"]))
    camera = dict(escala=s.uniform(0.85, 1.1),
                  desloc=s.uniform(-10, 10, 2),
                  luz=1.05 if lab else s.uniform(0.8, 1.15))
    angulos = {"em_pe": s.uniform(-15, 15),
               "girada": s.uniform(-180, 180)}
    ruido = int(s.integers(1_000_000))
    for pasta, angulo in angulos.items():
        foto, _, _, (ponta, peciolo) = fotografa(
            desenho, np.random.default_rng(ruido), fundo,
            angulo=angulo, **camera)
        Image.fromarray(foto).save(
            DESTINO / pasta / f"{n:04d}.jpg", quality=90)
        linhas.append([n, pasta, verdade, fundo,
                       round(angulo, 1), *np.round(ponta, 1),
                       *np.round(peciolo, 1)])
with open(DESTINO / "giradas.csv", "w", newline="",
          encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["foto", "pasta", "verdade", "fundo", "angulo",
                "ponta_x", "ponta_y", "peciolo_x",
                "peciolo_y"])
    w.writerows(linhas)
print(f"{len(classes)} folhas, {len(linhas)} fotos"
      f" em {DESTINO}")
