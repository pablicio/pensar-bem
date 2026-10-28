"""Ler um cartão inteiro de uma vez."""
import numpy as np
import torch

from leitora.decide import TEMPERATURA
from leitora.recorte import caixa, como_mnist, em_branco


def recorta(folha):
    """As caixas escritas, num lote, e onde cada uma estava."""
    imagens, onde = [], []
    for q in range(10):
        for k in range(3):
            tinta = caixa(folha, q, k)
            if not em_branco(tinta):
                imagens.append(como_mnist(tinta))
                onde.append((q, k))
    return torch.from_numpy(np.stack(imagens)), onde


@torch.inference_mode()
def le_cartao(modelo, folha):
    """As dez respostas: texto, número e confiança."""
    imagens, onde = recorta(folha)
    p = (modelo(imagens) / TEMPERATURA).softmax(dim=1)
    confianca, digito = p.max(dim=1)
    textos = [[" "] * 3 for _ in range(10)]
    conf = [1.0] * 10
    for (q, k), d, c in zip(onde, digito.tolist(),
                            confianca.tolist()):
        textos[q][k] = str(d)
        conf[q] *= c
    saida = []
    for q in range(10):
        texto = "".join(textos[q])
        numero = texto.lstrip()
        lido = (None if numero == "" else "inválida"
                if " " in numero else int(numero))
        saida.append((texto, lido, conf[q]))
    return saida
