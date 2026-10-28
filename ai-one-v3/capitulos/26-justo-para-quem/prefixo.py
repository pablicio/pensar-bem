from regioes import com_regiao

t = com_regiao()
fixo = t[t["prefixo"] > 0]
print(f"telefone fixo: {len(fixo) / len(t):.0%} dos pedidos")
regioes = fixo.groupby("prefixo")["regiao"].nunique()
print(f"prefixos de fixo: {len(regioes)};"
      f" com uma região só: {(regioes == 1).sum()}")
print(fixo.groupby("regiao")["prefixo"].unique().to_string())
