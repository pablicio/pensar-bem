from regra_jussara import carteira, regras_da_jussara

t = carteira()
t = t[t["data_concessao"].dt.year == 2024]
aprova = regras_da_jussara(t).all(axis=1)
noventa = t["data_atraso_90"].notna()
print(f"a regra aprovaria {aprova.mean():.0%} de {len(t):,}")
print(f"90 dias, aprovados: {noventa[aprova].mean():.1%}")
print(f"90 dias, recusados: {noventa[~aprova].mean():.1%}")
