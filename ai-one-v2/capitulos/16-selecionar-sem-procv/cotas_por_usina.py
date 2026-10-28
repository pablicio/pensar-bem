import pandas as pd

cad = pd.read_excel("dados/brutos/cadastro_cooperados.xlsx",
                    dtype={"CPF": "string"})
ativos = cad[cad["Situação"] == "Ativo"]
print(ativos["Usina"].value_counts())
for usina in ativos["Usina"].unique():
    da_usina = ativos["Usina"] == usina
    soma = ativos.loc[da_usina, "Cota (%)"].sum()
    print(f"{usina:17} {soma:9.4f}%")
