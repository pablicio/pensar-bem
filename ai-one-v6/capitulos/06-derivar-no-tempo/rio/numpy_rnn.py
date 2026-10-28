"""As células recorrentes escritas à mão, em NumPy."""
import numpy as np


def rnn_inicia(entradas, estado, sorteio, escala=None):
    """Os pesos de uma RNN: W_x, W_h e b."""
    escala = escala or 1 / np.sqrt(estado)
    return {"Wx": sorteio.normal(0, escala,
                                 (estado, entradas)),
            "Wh": sorteio.normal(0, escala, (estado, estado)),
            "b": np.zeros(estado)}


def rnn_passo(p, x, h):
    """Um passo: o estado novo, da entrada e do antigo."""
    return np.tanh(p["Wx"] @ x + p["Wh"] @ h + p["b"])


def rnn(p, xs, h=None):
    """Roda a sequência inteira e devolve todos os estados."""
    h = np.zeros(len(p["b"])) if h is None else h
    estados = []
    for x in xs:
        h = rnn_passo(p, x, h)
        estados.append(h)
    return np.array(estados)


def rnn_previsao(p, xs):
    """Lê a sequência e prevê um número pelo último estado."""
    estados = rnn(p, xs)
    return p["wy"] @ estados[-1] + p["c"], estados


def rnn_gradiente(p, xs, alvo, truncar=None):
    """A perda (previsto - alvo)² e o gradiente de cada peso,
    pela retropropagação no tempo."""
    previsto, estados = rnn_previsao(p, xs)
    erro = previsto - alvo
    g = {nome: np.zeros_like(peso) for nome, peso in p.items()}
    g["wy"] = 2 * erro * estados[-1]
    g["c"] = 2 * erro
    delta = 2 * erro * p["wy"]          # dL/dh no último passo
    zero = np.zeros(len(p["b"]))
    passos = len(xs) if truncar is None else truncar
    for t in range(len(xs) - 1, len(xs) - 1 - passos, -1):
        antes = estados[t - 1] if t > 0 else zero
        da = delta * (1 - estados[t] ** 2)  # pela tangente
        g["Wx"] += np.outer(da, xs[t])
        g["Wh"] += np.outer(da, antes)
        g["b"] += da
        delta = p["Wh"].T @ da          # para o passo anterior
    return erro ** 2, g
