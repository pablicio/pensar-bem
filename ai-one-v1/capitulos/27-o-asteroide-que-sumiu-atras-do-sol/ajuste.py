import matplotlib.pyplot as plt

from minimos import descida, perda, solucao_fechada
from vendidos import notas_e_precos

pares = notas_e_precos(2026, 200)
a_d, b_d, historico = descida(pares, 0.01, 5000)
a_f, b_f = solucao_fechada(pares)
for nome, a, b in [("descida", a_d, b_d),
                   ("fechada", a_f, b_f),
                   ("do Beto", 15, -30)]:
    print(f"{nome:8} a = {a:7.3f}  b = {b:7.3f}  "
          f"perda {perda(pares, a, b):6.2f}")

plt.figure(figsize=(6, 3.5))
plt.plot(range(1, 5001), historico)
plt.yscale("log")
plt.xlabel("passo da descida")
plt.ylabel("perda (R$²)")
plt.savefig("perda.png", dpi=300, bbox_inches="tight")

plt.figure(figsize=(6, 3.5))
plt.scatter([x for x, _ in pares], [y for _, y in pares],
            s=8, color="0.5")
ns = [3, 10]
plt.plot(ns, [a_f * x + b_f for x in ns],
         label="mínimos quadrados")
plt.plot(ns, [15 * x - 30 for x in ns], "--",
         label="regra do Beto")
plt.xlabel("nota de estado")
plt.ylabel("preço de venda (R$)")
plt.legend()
plt.savefig("reta_ajustada.png", dpi=300, bbox_inches="tight")
