import numpy as np
import torch

from lauber.acervo import carrega, grade
from lauber.vizinhos import carrega_npz, normaliza, vizinho

acervo, _ = carrega()
catalogo = carrega_npz("catalogo")      # 3000 estampas
amostra = carrega_npz("synapsys")       # as "100% originais"

for base_nome, base in (("acervo", acervo),
                        ("catálogo", catalogo)):
    for espelho in (False, True):
        qual, quanto = vizinho(amostra, base, espelho)
        texto = "  ".join(f"{q:5d} {s:.4f}"
                          for q, s in zip(qual, quanto))
        modo = "com espelho" if espelho else "sem espelho"
        print(f"{base_nome:8} {modo}: {texto}")

# o chão: quão parecidas são duas estampas diferentes
c = normaliza(catalogo)
s = c @ c.T
np.fill_diagonal(s, -1)
q = np.quantile(s.max(axis=1), [0.5, 0.99])
print(f"catálogo contra ele mesmo: mediana {q[0]:.4f},"
      f" 1% acima de {q[1]:.4f}")

# o retoque: espelhada = a * original + b, pixel a pixel
qual, _ = vizinho(amostra, catalogo, espelho=True)
desfeitas = []
for x, original in zip(amostra.flip(3), catalogo[qual]):
    a, b = np.polyfit(original.flatten().numpy(),
                      x.flatten().numpy(), 1)
    print(f"retoque: {a:.3f} x original + {b:.3f}")
    desfeitas.append(((x - b) / a).clamp(0, 1))
grade(torch.cat([amostra, torch.stack(desfeitas),
                 catalogo[qual]]), "synapsys.png", colunas=3)
