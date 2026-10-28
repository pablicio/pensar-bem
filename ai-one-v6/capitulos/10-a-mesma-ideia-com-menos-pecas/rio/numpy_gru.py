"""A GRU escrita à mão, em NumPy."""
import numpy as np

from rio.numpy_lstm import sigmoide


def gru_inicia(entradas, estado, sorteio):
    """Wzr: as portas de atualização e de reinício juntas;
    Wn: o candidato."""
    escala = 1 / np.sqrt(estado)
    S, E = estado, entradas
    p = {"Wzr": sorteio.normal(0, escala, (2 * S, E + S)),
         "bzr": np.zeros(2 * S),
         "Wn": sorteio.normal(0, escala, (S, E + S)),
         "bn": np.zeros(S)}
    p["bzr"][:S] = 1.0        # a atualização começa guardando
    return p


def gru(p, xs):
    """Roda a sequência e guarda o que a volta vai precisar."""
    S = len(p["bn"])
    h = np.zeros(S)
    passos = []
    for x in xs:
        zr = sigmoide(p["Wzr"] @ np.concatenate([x, h])
                      + p["bzr"])
        z, r = zr[:S], zr[S:]        # atualização e reinício
        n = np.tanh(p["Wn"] @ np.concatenate([x, r * h])
                    + p["bn"])       # o candidato
        passos.append((x, h, z, r, n))
        h = z * h + (1 - z) * n
    return passos, h


def gru_previsao(p, xs):
    """Lê a sequência e prevê um número pelo último estado."""
    passos, h = gru(p, xs)
    return p["wy"] @ h + p["c"], (passos, h)


def gru_gradiente(p, xs, alvo):
    """A perda (previsto - alvo)² e o gradiente dos pesos."""
    previsto, (passos, h) = gru_previsao(p, xs)
    erro = previsto - alvo
    g = {nome: np.zeros_like(v) for nome, v in p.items()}
    g["wy"], g["c"] = 2 * erro * h, 2 * erro
    dh = 2 * erro * p["wy"]
    for x, h_ant, z, r, n in reversed(passos):
        dn = dh * (1 - z) * (1 - n ** 2)
        dz = dh * (h_ant - n) * z * (1 - z)
        g["Wn"] += np.outer(dn, np.concatenate([x, r * h_ant]))
        g["bn"] += dn
        d_rh = (p["Wn"].T @ dn)[len(x):]
        dr = d_rh * h_ant * r * (1 - r)
        dzr = np.concatenate([dz, dr])
        g["Wzr"] += np.outer(dzr, np.concatenate([x, h_ant]))
        g["bzr"] += dzr
        dh = (dh * z + d_rh * r
              + (p["Wzr"].T @ dzr)[len(x):])
    return erro ** 2, g
