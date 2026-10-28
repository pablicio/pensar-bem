"""O laço de treino do volume 4, para as folhas."""
import random

import numpy as np
import torch
from torch.utils.data import DataLoader


def fixar_semente(semente, nucleos=1):
    """Todas as fontes de acaso, e quantos núcleos usar."""
    random.seed(semente)
    np.random.seed(semente)
    torch.manual_seed(semente)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(nucleos)


def lotes(dados, tamanho, semente=None):
    """Lotes sorteados com sorteador próprio, ou em ordem."""
    if semente is None:
        return DataLoader(dados, batch_size=tamanho)
    sorteador = torch.Generator().manual_seed(semente)
    return DataLoader(dados, batch_size=tamanho, shuffle=True,
                      generator=sorteador)


def treinar_epoca(modelo, carregador, otimizador, perda_fn):
    """Uma passada pelos lotes; devolve a perda média."""
    modelo.train()
    total, n = 0.0, 0
    for x, y in carregador:
        otimizador.zero_grad()
        perda = perda_fn(modelo(x), y)
        perda.backward()
        otimizador.step()
        total += perda.item() * len(y)
        n += len(y)
    return total / n


@torch.no_grad()
def prever(modelo, carregador):
    """As classes previstas e as certas, de todos os lotes."""
    modelo.eval()
    previstas, certas = [], []
    for x, y in carregador:
        previstas.append(modelo(x).argmax(dim=1))
        certas.append(y)
    return torch.cat(previstas), torch.cat(certas)


def acuracia(modelo, carregador):
    previstas, certas = prever(modelo, carregador)
    return (previstas == certas).float().mean().item()
