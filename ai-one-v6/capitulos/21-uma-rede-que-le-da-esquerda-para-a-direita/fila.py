import numpy as np
import pandas as pd
import torch

from rio.leitor import Leitor, preenche, probabilidades
from rio.texto import Vocabulario, mensagens, palavras, parte

POR_HORA = 110                   # o ritmo de leitura da Júlia
tab = mensagens()
voc = Vocabulario(parte(tab, "treino")["texto"], palavras)
modelo = Leitor(len(voc))
modelo.load_state_dict(torch.load("leitor.pt"))
noite = tab[(tab["data_hora"] >= "2026-10-14 19:00")
            & (tab["data_hora"] < "2026-10-15 07:00")]
chegada = noite["data_hora"].to_numpy()
risco = probabilidades(modelo, *preenche(voc, noite["texto"]))
risco = risco[:, 0]


def le(prioridade):
    """A hora em que cada mensagem é lida: a cada vez, a de
    maior prioridade entre as que já chegaram."""
    passo = pd.Timedelta(hours=1) / POR_HORA
    agora, lida = chegada[0], np.full(len(chegada), None)
    while (lida == None).any():         # noqa: E711
        fila = np.flatnonzero((lida == None)
                              & (chegada <= agora))
        if len(fila) == 0:
            agora = chegada[(lida == None)].min()
            continue
        lida[fila[np.argmax(prioridade[fila])]] = agora
        agora = agora + passo
    return pd.to_datetime(lida)


ivone = np.flatnonzero(noite["texto"].str.endswith("ivone"))[0]
de_risco = (noite["verdade"] == "risco").to_numpy()
chegou = -np.arange(len(chegada), dtype=float)
for nome, prioridade in [("ordem de chegada", chegou),
                         ("maior P(risco)", risco)]:
    lida = le(prioridade)
    espera = (lida - chegada) / pd.Timedelta(minutes=1)
    print(f"{nome}: Dona Ivone lida às {lida[ivone]:%H:%M}")
    print(f"  as de risco esperam"
          f" {np.median(espera[de_risco]):.0f} min (mediana),"
          f" {espera[de_risco].max():.0f} (máximo)")
print(f"P(risco) da Dona Ivone: {risco[ivone]:.2f}")
