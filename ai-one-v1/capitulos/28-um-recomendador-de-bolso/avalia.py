from loja import gerar_loja
from recomenda import recomendar, similaridades

discos, compras = gerar_loja(2027)
n = len(discos)
treino = [c[:-1] for c in compras]  # menos a última compra
escondida = [c[-1] for c in compras]  # a última, para conferir

sim = similaridades(treino, n)
vendas = [0] * n
for c in treino:
    for d in c:
        vendas[d] += 1
ordem = sorted(zip(vendas, range(n)), reverse=True)
ranking = [d for _, d in ordem]

acertos_rec = acertos_pop = 0
for c, ultima in zip(treino, escondida):
    if ultima in recomendar(c, sim):
        acertos_rec += 1
    if ultima in [d for d in ranking if d not in c][:10]:
        acertos_pop += 1
print(f"taxa de acerto em 10, recomendador:  "
      f"{acertos_rec / len(compras):.3f}")
print(f"taxa de acerto em 10, mais vendidos: "
      f"{acertos_pop / len(compras):.3f}")
