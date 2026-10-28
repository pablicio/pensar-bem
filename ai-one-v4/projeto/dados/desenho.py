"""Desenha um dígito de traços com a mão de uma pessoa."""
import numpy as np
from PIL import Image, ImageDraw

LADO = 112                       # desenha grande, reduz depois


def desenha(tracos, sorteio, espessura):
    """Os traços, deformados ao acaso, de 0 a 255."""
    giro = np.radians(sorteio.normal(0, 10))
    incl = sorteio.normal(0, 0.25)
    escala = sorteio.uniform(0.7, 1.15, size=2)
    M = np.array([[np.cos(giro), -np.sin(giro)],
                  [np.sin(giro), np.cos(giro)]])
    M = M @ np.array([[1, incl], [0, 1]]) * escala
    img = Image.new("L", (LADO, LADO), 0)
    lapis = ImageDraw.Draw(img)
    for t in tracos:
        p = np.array(t) - 0.5
        p = p + sorteio.normal(0, 0.018, p.shape)   # tremor
        p = (p @ M.T + 0.5) * LADO * 0.7 + LADO * 0.15
        lapis.line([tuple(q) for q in p], fill=255,
                   width=int(espessura), joint="curve")
    return img
