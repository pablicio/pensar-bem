import matplotlib.pyplot as plt

from integral import riemann, trapezio
from promocao import vendas_por_hora

print("    n    retângulos     trapézios")
for n in [1, 4, 10, 20, 100, 1000]:
    r = riemann(vendas_por_hora, 0, 20, n)
    t = trapezio(vendas_por_hora, 0, 20, n)
    print(f"{n:5d}  {r:12.2f}  {t:12.2f}")

ts = [i / 10 for i in range(201)]
plt.figure(figsize=(6, 3.6))
plt.bar([2 * i for i in range(10)],
        [vendas_por_hora(2 * i) for i in range(10)],
        width=2, align="edge", color="0.85", edgecolor="0.4")
plt.plot(ts, [vendas_por_hora(t) for t in ts])
plt.xlabel("horas desde o início da promoção")
plt.ylabel("vendas (R$ por hora)")
plt.savefig("retangulos.png", dpi=300, bbox_inches="tight")
