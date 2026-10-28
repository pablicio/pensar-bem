from gerar_balcao import vendas_do_mes
from resumo import desvio_padrao, media, mediana, percentil

novembro = vendas_do_mes(1111, 112)
dezembro = vendas_do_mes(1225, 115) + [9000.00]  # e a raridade

print("                  média  mediana   desvio      p90")
for nome, v in [("novembro", novembro), ("dezembro", dezembro),
                ("dez. sem o raro", dezembro[:-1])]:
    print(f"{nome:15s} {media(v):8.2f} {mediana(v):8.2f}"
          f" {desvio_padrao(v):8.2f} {percentil(v, 90):8.2f}")
alta = media(dezembro) / media(novembro) - 1
print(f"alta do ticket médio: {alta:.0%}")
