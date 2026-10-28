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
