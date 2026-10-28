from fatoracao import matriz, recomendar_fatores, treinar
from loja import gerar_loja

discos, compras = gerar_loja(2027)
treino = [c[:-1] for c in compras]
r = matriz(treino, len(discos))
for lam in [0, 3, 6]:
    p, q, b, h = treinar(r, k=6, eta=0.004, lam=lam,
                         epocas=300, semente=2)
    acertos = sum(1 for c, t in enumerate(compras)
                  if t[-1] in recomendar_fatores(c, treino[c],
                                                 p, q, b))
    print(f"lambda {lam}: perda {h[-1]:.1f}, "
          f"acerto {acertos / len(compras):.3f}")
