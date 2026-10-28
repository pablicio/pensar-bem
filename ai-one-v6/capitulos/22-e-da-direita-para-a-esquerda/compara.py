import time

import numpy as np
import torch

from rio.bayes import Bayes
from rio.leitor import (Leitor, preenche, probabilidades,
                        treina_leitor)
from rio.provinha import PROVINHA
from rio.texto import (CLASSES, Vocabulario, mensagens,
                       palavras, parte)

tab = mensagens()
treino, valid, teste = (parte(tab, p) for p in
                        ("treino", "validacao", "teste"))
voc = Vocabulario(treino["texto"], palavras)
textos_p, classes_p = zip(*PROVINHA)
y_t = teste["verdade"].map(CLASSES.index).to_numpy()
y_p = np.array([CLASSES.index(c) for c in classes_p])
# perguntas sobre boatos: "é verdade que...?" é info
pergunta = (teste["texto"].str.contains("verdade")
            & (teste["verdade"] == "info")).to_numpy()
vizinho = 3                  # o vizinho de 80 anos


def mede(nome, p_t, p_p, segundos):
    certo_p = p_p.argmax(1) == y_p
    return [nome, np.mean(p_t.argmax(1) == y_t),
            np.mean(p_t[pergunta].argmax(1) == 2),
            certo_p.sum(), (certo_p & (y_p == 0)).sum(),
            p_p[vizinho, 0], segundos]


def lote(t, coluna):
    x, n = preenche(voc, t["texto"])
    y = t[coluna].map(CLASSES.index).to_numpy()
    return x, n, torch.tensor(y.copy())


inicio = time.time()
bayes = Bayes(treino["texto"], treino["classe"])
b_t = bayes.probabilidades(teste["texto"])
b_p = bayes.probabilidades(textos_p)
linhas = [mede("Naive Bayes", b_t, b_p, time.time() - inicio)]
tr, va = lote(treino, "classe"), lote(valid, "classe")
x_t, n_t = preenche(voc, teste["texto"])
x_p, n_p = preenche(voc, textos_p)
MODELOS = {"LSTM": {},
           "bidirecional": {"bidirecional": True},
           "bi, 2 camadas": {"bidirecional": True,
                             "camadas": 2, "dropout": 0.3}}
for nome, opcoes in MODELOS.items():
    for semente in range(5):
        torch.manual_seed(semente)
        modelo = Leitor(len(voc), **opcoes)
        inicio = time.time()
        treina_leitor(modelo, tr, va)
        segundos = time.time() - inicio
        p_t = probabilidades(modelo, x_t, n_t)
        p_p = probabilidades(modelo, x_p, n_p)
        linhas.append(mede(nome, p_t, p_p, segundos))
        if nome == "LSTM":
            media_t, media_p = (p_t + b_t) / 2, (p_p + b_p) / 2
            linhas.append(mede("média LSTM+Bayes", media_t,
                               media_p, segundos))
print(f"teste: {len(y_t)} mensagens, {pergunta.sum()}"
      " perguntas sobre boatos")
print("modelo             teste pergun. prov. faixa risco"
      " viz.    s")
for nome in dict.fromkeys(l[0] for l in linhas):
    m = [l[1:] for l in linhas if l[0] == nome]
    t, q, c, r, v, s = np.mean(m, axis=0)
    faixa = f"{min(x[2] for x in m)}-{max(x[2] for x in m)}"
    print(f"{nome:16}{t:8.2%}{q:8.2%}{c:6.1f}{faixa:>6}"
          f"{r:6.1f}{v:5.2f}{s:5.0f}")
