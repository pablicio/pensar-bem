from rateio.calculo import credito
from rateio.geracao import geracao_diaria
from rateio.leitura import ler_cadastro

leituras = geracao_diaria("2027-02")
por_usina = leituras.groupby("usina")["kwh"].sum().round(3)
cad = ler_cadastro()
dirceu = cad[cad["Código"] == 2959].iloc[0]
geracao = por_usina[dirceu["Usina"]]
kwh, reais = credito(geracao, dirceu["Cota (%)"])
print(f"Dirceu: {kwh:,.2f} kWh, R$ {reais:,.2f}")
