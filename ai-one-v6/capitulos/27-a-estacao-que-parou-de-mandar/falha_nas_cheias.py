import numpy as np
import pandas as pd
import torch

from rio.alerta import maximo_previsto
from rio.avalia import parte
from rio.cota import grupos, julga
from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.estacoes import colunas_de
from rio.quantis import preve_quantis
from rio.treino import conjunto

H = tuple(range(1, 13))
tab = com_subidas(tabela())
nivel = tab["cidade"]
teste = parte(nivel, "teste")
acima = teste.interpolate(limit=3) >= 5.5
comeca = acima & ~acima.shift(1, fill_value=False)
cheias = grupos(teste.index[comeca], "72h")
# Apiúna fora do ar de 12 h antes a 12 h depois de cada cheia
fora = pd.Series(False, index=tab.index)
for inicio, _ in cheias:
    fora[inicio - pd.Timedelta("12h"):
         inicio + pd.Timedelta("12h")] = True


def previsao(tabela_usada, arquivo):
    escalada = Escala(tabela_usada).aplica(tabela_usada)
    x, _, horas = conjunto(escalada, nivel, "teste", H)
    modelo = Previsor(x.shape[2], range(36), estado=64)
    modelo.load_state_dict(torch.load(arquivo))
    q = preve_quantis(modelo, x)
    agora = nivel.loc[horas].to_numpy()
    p = pd.DataFrame({"teto": maximo_previsto(agora, q, 2),
                      "mediana": maximo_previsto(agora, q, 1),
                      "largura": q[:, -1, 2] - q[:, -1, 0]},
                     index=horas)
    return p.reindex(completa_horas)


completa_horas = conjunto(tab, nivel, "teste", H)[2]
completa = previsao(tab, "plantao.pt")
# janelas que tocam a falta: as 71 horas depois dela também
tocada = fora.rolling(72, min_periods=1).max().astype(bool)
tocada = tocada.loc[completa.index]
ultimo = tab.copy()
for c in colunas_de("apiuna"):
    ultimo.loc[fora, c] = np.nan
ultimo["apiuna"] = ultimo["apiuna"].ffill()
ultimo[["sobe_apiuna", "chuva_apiuna"]] = \
    ultimo[["sobe_apiuna", "chuva_apiuna"]].fillna(0.0)
sem = tab.drop(columns=colunas_de("apiuna"))
reserva = previsao(sem, "sem_apiuna.pt")
POLITICAS = {
    "sem falha": completa,
    "não prever": completa.where(~tocada, axis=0),
    "último valor": completa.where(
        ~tocada, previsao(ultimo, "plantao.pt"), axis=0),
    "modelo sem Apiúna": completa.where(~tocada, reserva,
                                         axis=0)}
real = pd.concat([nivel.shift(-h) for h in H], axis=1)
real = real.max(axis=1)
real = real.loc[completa.index]
print("política           antecedência (h)  falsos   viés")
for nome, prev in POLITICAS.items():
    teto = prev["teto"]
    vies = (prev["mediana"] - real)[tocada].mean()
    alarme = (teto >= 5.5).astype(float).where(teto.notna())
    alarme = alarme.ffill().fillna(0.0)
    cheias_, ant, _, falsos = julga(
        nivel, np.where(alarme > 0, 99.0, 0.0), alarme.index)
    texto = " ".join(f"{a:2.0f}" for a in ant)
    vies = "—" if np.isnan(vies) else f"{vies * 100:.0f}"
    print(f"{nome:18} {texto:17} {falsos:6d} {vies:>6} cm")
print("largura da faixa em 12 h, nas horas da falta:")
for nome, prev in (("completa", completa),
                   ("sem Apiúna", reserva)):
    largura = prev["largura"][tocada].mean() * 100
    print(f"  {nome:10} {largura:4.0f} cm")
