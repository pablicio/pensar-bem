import pandas as pd
import torch

from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.estacoes import ESTACOES, colunas_de
from rio.plantao import Plantao
from rio.serie import ler, nivel_cidade

tele = ler("telemetria").loc["2023-12-28":"2024-01-09"].copy()
tele["nivel_cidade"] = nivel_cidade().loc[tele.index] * 100
historico = com_subidas(tabela())


def carrega(arquivo, tab):
    modelo = Previsor(tab.shape[1], range(36), estado=64)
    modelo.load_state_dict(torch.load(arquivo))
    return modelo, Escala(tab)


reservas = {}
for e in ESTACOES:
    sem = historico.drop(columns=colunas_de(e))
    reservas[e] = carrega(f"sem_{e}.pt", sem)
plantao = Plantao(*carrega("plantao.pt", historico), historico,
                  reservas)
linhas = [plantao.hora(tele.loc[:agora]) for agora in
          pd.date_range("2024-01-05 18:00", "2024-01-06 16:00",
                        freq="h")]
registro = pd.DataFrame(linhas).set_index("hora")
print("hora      nível  teto 12 h  largura  fora    alarme")
for hora, l in registro.iterrows():
    nivel, teto, largura = l["nivel"], l["teto"], l["largura"]
    fora = l["fora"] or "-"
    alarme = "sim" if l["alarme"] else "não"
    print(f"{hora:%d/%m %Hh} {nivel:6.2f} {teto:9.2f}"
          f" {largura * 100:6.0f} cm  {fora:7} {alarme}")
