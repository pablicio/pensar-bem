from pathlib import Path

import pandas as pd

from rateio import manifesto
from rateio.calculo import TARIFA
from rateio.geracao import geracao_diaria
from rateio.leitura import BRUTOS, ler_cadastro
from rateio.limpeza import cpf_normalizado

leituras = geracao_diaria("2027-02")
por_usina = leituras.groupby("usina")["kwh"].sum().round(3)
cad = ler_cadastro()
ativos = cad[cad["Situação"] == "Ativo"]
geracao = ativos["Usina"].map(por_usina)
kwh = (geracao * ativos["Cota (%)"] / 100).round(2)
rateio = pd.DataFrame({"CPF": cpf_normalizado(ativos["CPF"]),
                       "Nome": ativos["Nome"], "kWh": kwh,
                       "Valor": (kwh * TARIFA).round(2)})

saida = Path("dados/processados/rateio_2027-02_corrigido.csv")
saida.parent.mkdir(exist_ok=True)
rateio.to_csv(saida, index=False)
entradas = [BRUTOS / "cadastro_cooperados.xlsx",
            *sorted(BRUTOS.glob("inversores/*/*2027-02*"))]
origem = manifesto.registrar_origem(saida, entradas,
                                    "fevereiro_corrigido.py")
total = rateio["Valor"].sum()
print(f"{len(rateio)} cooperados, R$ {total:,.2f}")
n = len(origem["entradas"])
print(f"{n} entradas registradas em {saida.name}.origem.json")
