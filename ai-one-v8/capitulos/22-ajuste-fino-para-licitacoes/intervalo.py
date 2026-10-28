import numpy as np
import torch

salvo = torch.load("previsoes.pt", weights_only=False)
y = salvo["y"].numpy()
prev = {n: np.asarray(p)
        for n, p in salvo["previsoes"].items()}


def f1(p, y):
    vp = ((p == 1) & (y == 1)).sum()
    fp = ((p == 1) & (y == 0)).sum()
    fn = ((p == 0) & (y == 1)).sum()
    return 2 * vp / max(2 * vp + fp + fn, 1)


rng = np.random.default_rng(0)
# 2.000 reamostras do teste, com reposição
amostras = rng.integers(0, len(y), (2000, len(y)))
print("F1 e intervalo de 95% (bootstrap, 2.000 reamostras)")
f1s = {}
for nome, p in prev.items():
    f1s[nome] = np.array([f1(p[i], y[i]) for i in amostras])
    baixo, alto = np.percentile(f1s[nome], [2.5, 97.5])
    print(f"  {nome:19} {f1(p, y):.3f}"
          f"  [{baixo:.3f}, {alto:.3f}]")

print("diferenças pareadas (mesmas reamostras)")
for a, b in [("ajuste completo", "sem pré-treino"),
             ("ajuste completo", "TF-IDF e logística")]:
    dif = f1s[a] - f1s[b]
    baixo, alto = np.percentile(dif, [2.5, 97.5])
    centro = f1(prev[a], y) - f1(prev[b], y)
    print(f"  {a} - {b}:")
    print(f"    {centro:+.3f}  [{baixo:+.3f}, {alto:+.3f}]")
