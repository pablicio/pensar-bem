import numpy as np
import pandas as pd
import torch

from rio.entradas import Escala, com_subidas, tabela
from rio.extrator import (Extrator, confere, registro,
                          vocabularios)
from rio.leitor import preenche
from rio.modelos import Previsor
from rio.estacoes import ESTACOES, colunas_de
from rio.plantao import Plantao
from rio.serie import ler, nivel_cidade
from rio.texto import mensagens, parte
from rio.triagem import carrega, triagem

INICIO, FIM = "2023-11-17 00:00", "2023-11-19 06:00"
POR_HORA = 110                   # o ritmo de leitura da Júlia
HORA = pd.Timedelta("1h")
# o rio: o plantão do capítulo 27, com as reservas
tele = ler("telemetria").loc["2023-11-10":FIM].copy()
tele["nivel_cidade"] = nivel_cidade().loc[tele.index] * 100
historico = com_subidas(tabela())


def rede(arquivo, tab):
    modelo = Previsor(tab.shape[1], range(36), estado=64)
    modelo.load_state_dict(torch.load(arquivo))
    return modelo, Escala(tab)


reservas = {}
for e in ESTACOES:
    sem = historico.drop(columns=colunas_de(e))
    reservas[e] = rede(f"sem_{e}.pt", sem)
plantao = Plantao(*rede("plantao.pt", historico), historico,
                  reservas)
horas = pd.date_range(INICIO, FIM, freq="h")
rio = pd.DataFrame([plantao.hora(tele.loc[:h]) for h in horas])
rio = rio.set_index("hora")
# as mensagens: triagem e pilha dos boatos
tab = mensagens()
msg = tab[(tab["data_hora"] >= INICIO)
          & (tab["data_hora"] <= FIM)].reset_index(drop=True)
voc, leitor, bayes = carrega()
p = triagem(msg["texto"], voc, leitor, bayes)
pilha = p[:, 3] > 0.5
chegada = msg["data_hora"].to_numpy()


def le(prioridade, ativas):
    """Os minutos que cada mensagem ativa espera até a Júlia
    ler: a cada vez, a de maior prioridade que já chegou."""
    lida = np.full(len(msg), np.datetime64("NaT"), "M8[ns]")
    agora = chegada[0]
    passo = np.timedelta64(3600 // POR_HORA, "s")
    espera = ativas.copy()
    while espera.any():
        fila = np.flatnonzero(espera & (chegada <= agora))
        if len(fila) == 0:
            agora = chegada[espera].min()
            continue
        i = fila[np.argmax(prioridade[fila])]
        lida[i], espera[i] = agora, False
        agora = agora + passo
    return (lida - chegada) / np.timedelta64(1, "m")


# os pedidos: o extrator do capítulo 24 preenche a planilha
treino = parte(tab[tab["verdade"].isin(["risco", "ajuda"])],
               "treino")
registros = [registro(l) for _, l in treino.iterrows()]
entrada, saida = vocabularios(treino["texto"], registros)
extrator = Extrator(len(entrada), len(saida))
extrator.load_state_dict(torch.load("extrator.pt"))
e_pedido = (p[:, :2].sum(axis=1) > 0.5) & ~pilha
textos = msg["texto"][e_pedido].tolist()
x, n = preenche(entrada, textos, maximo=240)
gerado = extrator.extrai(x, n, saida)
suspeito = np.array([confere(g, t)[1]
                     for g, t in zip(gerado, textos)])
# o registro do simulado
msg["pilha"] = pilha
msg["p_risco"] = p[:, 0].round(3)
msg["espera_triagem"] = le(p[:, 0], ~pilha)
msg["espera_chegada"] = le(-np.arange(len(msg), dtype=float),
                           np.ones(len(msg), bool))
msg["suspeito"] = pd.Series(suspeito,
                            index=msg.index[e_pedido])
msg.to_csv("simulado_mensagens.csv", index=False)
rio.to_csv("simulado_rio.csv")
print("hora       nível  teto  fora    alarme  msgs  pilha")
for h in horas[::3]:
    r = rio.loc[h]
    nesta = ((chegada >= np.datetime64(h))
             & (chegada < np.datetime64(h + 3 * HORA)))
    teto = "" if pd.isna(r["teto"]) else f"{r['teto']:.2f}"
    fora = r["fora"] or "-"
    alarme = "sim" if r["alarme"] else "não"
    na_pilha = (nesta & pilha).sum()
    nivel = r["nivel"]
    print(f"{h:%d/%m %Hh} {nivel:6.2f} {teto:>5}  {fora:7}"
          f" {alarme:6} {nesta.sum():5d} {na_pilha:6d}")
