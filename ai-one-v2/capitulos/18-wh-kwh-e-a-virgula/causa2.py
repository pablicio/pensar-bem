from rateio.calculo import TARIFA
from rateio.leitura import ler_cadastro, ler_corumba, ler_envio
from rateio.limpeza import corumba_em_kwh, cpf_normalizado

a = ler_corumba("2027-02")
planilha = round(float(a["Energia"].sum() / 1000), 3)
certa = round(float(corumba_em_kwh(a).sum()), 3)
print(f"Corumbá pela planilha: {planilha:12,.3f} kWh")
print(f"Corumbá corrigida:     {certa:12,.3f} kWh")

cad = ler_cadastro()
usina = cad[(cad["Situação"] == "Ativo")
            & (cad["Usina"] == "Corumbá de Goiás")]
kwh = (certa * usina["Cota (%)"] / 100).round(2)
certo = (kwh * TARIFA).round(2)

envio = ler_envio("2027-02")
chave = cpf_normalizado(envio["CPF"])
enviado = envio.set_index(chave)["Valor"]
cpfs = cpf_normalizado(usina["CPF"])
mandado = enviado.loc[cpfs].to_numpy()
diferenca = abs(mandado - certo)
print(f"{len(usina)} cooperados de Corumbá")
print(f"crédito que faltou: R$ {diferenca.sum():,.2f}")
