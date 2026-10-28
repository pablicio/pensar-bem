from loja import gerar_loja
from recomenda import recomendar, similaridades

discos, compras = gerar_loja(2027)
treino = [c[:-1] for c in compras]
sim = similaridades(treino, len(discos))
for n in [5, 10, 20]:
    acertos = sum(1 for c, todas in zip(treino, compras)
                  if todas[-1] in recomendar(c, sim, n))
    print(f"em {n:2}: {acertos / len(compras):.3f}")
