from risco.alvo import carteira

t = carteira()
safra = t["data_concessao"].dt.to_period("Q")
noventa = t["data_atraso_90"].notna()
taxa = noventa.groupby(safra).mean()
print("safra    chegaram a 90 dias até 12/3/2027")
for trimestre, valor in taxa.loc["2025Q1":].items():
    print(f"{trimestre}   {valor:6.1%}")
