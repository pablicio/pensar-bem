import matplotlib.pyplot as plt

from distribuicoes import normal
from gerar_balcao import vendas_do_mes
from resumo import desvio_padrao, media

totais = [sum(vendas_do_mes(dia, 30)) for dia in range(2000)]
m, s = media(totais), desvio_padrao(totais)
print(f"sábado de 30 vendas: média {m:.0f}, desvio {s:.0f}")
dentro = sum(1 for t in totais if abs(t - m) < 2 * s) / 2000
print(f"sábados a menos de 2 desvios da média: {dentro:.3f}")

xs = [m - 4 * s + i * s / 10 for i in range(81)]
plt.figure(figsize=(6, 3.5))
plt.hist(totais, bins=40, density=True, color="0.85",
         edgecolor="0.4")
plt.plot(xs, [normal(x, m, s) for x in xs])
plt.xlabel("faturamento de um sábado de 30 vendas (R$)")
plt.ylabel("densidade")
plt.savefig("dias.png", dpi=300, bbox_inches="tight")
