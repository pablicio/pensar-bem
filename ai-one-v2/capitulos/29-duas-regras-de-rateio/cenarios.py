from experimento import ENTRADAS, metricas, monta_tabela
from rateio import registro

tabela = monta_tabela()
print("consumo  crédito parado  muda de mão  perdem >10%")
for p in [0, 0.25, 0.5, 0.75, 1]:
    m = metricas(tabela, p)
    registro.registrar("regra mista", {"p_consumo": p}, m,
                       ENTRADAS)
    print(f"{p:>7.0%}  {m['credito_parado']:>14,.0f}"
          f"  {m['muda_de_mao']:>11,.0f}"
          f"  {m['perdem_mais_de_10pct']:>11}")
