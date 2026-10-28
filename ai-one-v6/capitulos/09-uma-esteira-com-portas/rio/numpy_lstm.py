"""A LSTM escrita à mão, em NumPy."""
import numpy as np


def sigmoide(z):
    return 1 / (1 + np.exp(-z))


def lstm_inicia(entradas, estado, sorteio):
    """Os pesos das quatro partes juntos: W tem 4S linhas, na
    ordem entrada, esquecimento, saída e candidato."""
    escala = 1 / np.sqrt(estado)
    S = estado
    p = {"W": sorteio.normal(0, escala, (4 * S, entradas + S)),
         "b": np.zeros(4 * S)}
    p["b"][S:2 * S] = 1.0     # o esquecimento começa aberto
    return p


def lstm(p, xs):
    """Roda a sequência e guarda, a cada passo, o que a volta
    no tempo vai precisar."""
    S = len(p["b"]) // 4
    h, c = np.zeros(S), np.zeros(S)
    passos = []
    for x in xs:
        z = p["W"] @ np.concatenate([x, h]) + p["b"]
        i = sigmoide(z[:S])            # porta de entrada
        f = sigmoide(z[S:2 * S])       # porta de esquecimento
        o = sigmoide(z[2 * S:3 * S])   # porta de saída
        g = np.tanh(z[3 * S:])         # o candidato a guardar
        passos.append((x, h, c, i, f, o, g))
        c = f * c + i * g              # a esteira
        h = o * np.tanh(c)
    return passos, h, c


def lstm_previsao(p, xs):
    """Lê a sequência e prevê um número pelo último estado."""
    passos, h, c = lstm(p, xs)
    return p["wy"] @ h + p["c"], (passos, h, c)


def lstm_gradiente(p, xs, alvo):
    """A perda (previsto - alvo)² e o gradiente dos pesos."""
    previsto, (passos, h, c) = lstm_previsao(p, xs)
    erro = previsto - alvo
    g_ = {n: np.zeros_like(v) for n, v in p.items()}
    g_["wy"], g_["c"] = 2 * erro * h, 2 * erro
    dh = 2 * erro * p["wy"]
    dc = np.zeros_like(c)
    for x, h_ant, c_ant, i, f, o, g in reversed(passos):
        c_t = f * c_ant + i * g
        tc = np.tanh(c_t)
        dc = dc + dh * o * (1 - tc ** 2)
        dz = np.concatenate([dc * g * i * (1 - i),
                             dc * c_ant * f * (1 - f),
                             dh * tc * o * (1 - o),
                             dc * i * (1 - g ** 2)])
        g_["W"] += np.outer(dz, np.concatenate([x, h_ant]))
        g_["b"] += dz
        dh = (p["W"].T @ dz)[len(x):]
        dc = dc * f                    # a esteira, para trás
    return erro ** 2, g_
