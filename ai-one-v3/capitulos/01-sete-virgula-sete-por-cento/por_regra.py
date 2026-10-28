from regra_jussara import carteira, regras_da_jussara

t = carteira()
t = t[t["data_concessao"].dt.year == 2025]
regras = regras_da_jussara(t)
noventa = t["data_atraso_90"].notna()
print("regra                            recusa  chegaram a 90")
for nome in regras.columns:
    recusa = ~regras[nome]
    if recusa.any():
        taxa = noventa[recusa].mean()
        print(f"{nome:32} {recusa.sum():6,} {taxa:14.1%}")
