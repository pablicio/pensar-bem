from experimento import metricas, monta_tabela

tabela = monta_tabela()
for pontos in range(25, 31):
    m = metricas(tabela, pontos / 100)
    print(f"{pontos}%: parado R$ {m['credito_parado']:>9,.0f},"
          f" perdem {m['perdem_mais_de_10pct']}")
