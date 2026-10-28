import pandas as pd

planilha = "dados/brutos/RATEIO_FINAL_v7_AGORA_VAI.xlsx"
par = pd.read_excel(planilha, sheet_name="Parâmetros")
coluna = par["Geração do mês (kWh)"]
geracao = par.set_index("Usina")[coluna.name].iloc[:3]
tarifa = coluna.iloc[4]

cad = pd.read_excel("dados/brutos/cadastro_cooperados.xlsx",
                    dtype={"CPF": "string"})
ativos = cad[cad["Situação"] == "Ativo"]
rateio = ativos.assign(
    kwh=(ativos["Usina"].map(geracao)
         * ativos["Cota (%)"] / 100).round(2))
rateio = rateio.assign(valor=(rateio["kwh"] * tarifa).round(2))

grandes = rateio.loc[(rateio["Tipo"] == "comercio")
                     & (rateio["valor"] > 500),
                     ["Nome", "Usina", "valor"]]
print(len(grandes), "comércios com mais de R$ 500")
print(grandes.sort_values("valor", ascending=False).head(4))
print(f"total do rateio: R$ {rateio['valor'].sum():,.2f}")
