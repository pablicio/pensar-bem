import matplotlib.pyplot as plt
import numpy as np

from rio.numpy_lstm import lstm_gradiente, lstm_inicia
from rio.numpy_lstm import lstm_previsao
from rio.numpy_rnn import rnn_gradiente, rnn_inicia
from rio.numpy_rnn import rnn_previsao
from rio.numpy_treino import adam_inicia, epoca, tarefa_soma

sorteio = np.random.default_rng(0)
x, y = tarefa_soma(sorteio, 2000, 50)
xv, yv = tarefa_soma(sorteio, 500, 50)
redes = {"RNN": (rnn_inicia, rnn_gradiente, rnn_previsao),
         "LSTM": (lstm_inicia, lstm_gradiente, lstm_previsao)}
treinadas = {}
print("época  " + "  ".join(f"{nome:>6}" for nome in redes))
erros = {nome: [] for nome in redes}
for nome, (inicia, gradiente, previsao) in redes.items():
    s = np.random.default_rng(1)
    p = inicia(2, 16, s)
    p["wy"], p["c"] = np.zeros(16), np.array(1.0)
    adam = adam_inicia(p)
    for _ in range(8):
        epoca(p, gradiente, x, y, s, 0.003, 1.0, adam)
        prev = np.array([previsao(p, q)[0] for q in xv])
        erros[nome].append(np.mean((prev - yv) ** 2))
    treinadas[nome] = (p, previsao)
for e in range(8):
    print(f"{e + 1:5d}  " + "  ".join(f"{erros[n][e]:6.4f}"
                                     for n in redes))

# quanto a previsão muda quando se mexe no número de cada hora
seq = xv[0].copy()
fig, ax = plt.subplots(figsize=(6, 3))
for nome, (p, previsao) in treinadas.items():
    efeito = []
    for t in range(50):
        mais, menos = seq.copy(), seq.copy()
        mais[t, 0] += 1e-4
        menos[t, 0] -= 1e-4
        efeito.append(abs(previsao(p, mais)[0]
                          - previsao(p, menos)[0]) / 2e-4)
    ax.semilogy(efeito, marker=".", label=nome)
    marcas = np.flatnonzero(seq[:, 1])
    print(nome, "efeito nas horas marcadas",
          [round(float(efeito[m]), 3) for m in marcas])
for m in np.flatnonzero(seq[:, 1]):
    ax.axvline(m, color="0.6", ls="--", lw=0.8)
ax.set_xlabel("hora da sequência")
ax.set_ylabel("efeito na previsão")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("sensibilidade.png", dpi=300)
