"""Lê o MNIST do formato IDX, o original de 1998, com NumPy."""
import gzip
from pathlib import Path

import numpy as np

PASTA = Path("dados/brutos/mnist")
PREFIXO = {"treino": "train", "teste": "t10k"}


def _idx(caminho):
    with gzip.open(caminho, "rb") as f:
        dados = f.read()
    dims = dados[3]                         # quantas dimensões
    # os tamanhos: inteiros de 4 bytes, o mais alto primeiro
    tamanhos = np.frombuffer(dados, ">u4", count=dims,
                             offset=4)
    inicio = 4 + 4 * dims
    valores = np.frombuffer(dados, np.uint8, offset=inicio)
    return valores.reshape(tamanhos)


def carregar(parte="treino"):
    """Imagens (n, 28, 28) de 0 a 255 e os rótulos (n,)."""
    p = PREFIXO[parte]
    imagens = _idx(PASTA / f"{p}-images-idx3-ubyte.gz")
    rotulos = _idx(PASTA / f"{p}-labels-idx1-ubyte.gz")
    return imagens, rotulos
