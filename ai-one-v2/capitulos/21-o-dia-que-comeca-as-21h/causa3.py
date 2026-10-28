import pandas as pd

from rateio.calculo import TARIFA
from rateio.fuso import cocalzinho_local
from rateio.geracao import dias_do_mes
from rateio.leitura import (ler_cadastro, ler_cocalzinho,
                            ler_envio)
from rateio.limpeza import cpf_normalizado

dias = ["2027-01-31"] + dias_do_mes("2027-02") + ["2027-03-01"]
b = ler_cocalzinho(dias)
positivo = b["energia_kwh"].clip(lower=0)

# como a macro fez: o horário escrito, janela de 05h às 19h
escrito = pd.to_datetime(b["inicio"].str.removesuffix("Z"))
no_mes = escrito.dt.strftime("%Y-%m") == "2027-02"
janela = (escrito.dt.hour >= 5) & (escrito.dt.hour < 19)
planilha = round(float(positivo[no_mes & janela].sum()), 3)

# como devia ser: o instante, no fuso de Brasília
local = cocalzinho_local(b["inicio"])
certa = round(float(positivo[local.dt.month == 2].sum()), 3)
print(f"Cocalzinho pela macro: {planilha:11,.2f} kWh")
print(f"Cocalzinho certa:      {certa:11,.2f} kWh")

cad = ler_cadastro()
usina = cad[(cad["Situação"] == "Ativo")
            & (cad["Usina"] == "Cocalzinho")]
certo = ((certa * usina["Cota (%)"] / 100).round(2)
         * TARIFA).round(2)
envio = ler_envio("2027-02")
chave = cpf_normalizado(envio["CPF"])
enviado = envio.set_index(chave)["Valor"]
mandado = enviado.loc[cpf_normalizado(usina["CPF"])].to_numpy()
faltou = abs(mandado - certo).sum()
print(f"{len(usina)} cooperados de Cocalzinho")
print(f"crédito que faltou: R$ {faltou:,.2f}")
