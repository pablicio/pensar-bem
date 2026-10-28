"""O laço de treino da leitora: reprodutível e retomável."""
import random

import numpy as np
import torch
from torch.utils.data import DataLoader


def fixar_semente(semente):
    """Todas as fontes de acaso, de uma vez."""
    random.seed(semente)
    np.random.seed(semente)
    torch.manual_seed(semente)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)


def lotes(dados, tamanho, semente=None):
    """Lotes sorteados com sorteador próprio, ou em ordem."""
    if semente is None:
        return DataLoader(dados, batch_size=tamanho)
    sorteador = torch.Generator().manual_seed(semente)
    return DataLoader(dados, batch_size=tamanho, shuffle=True,
                      generator=sorteador)


def treinar_epoca(modelo, carregador, otimizador, perda_fn):
    modelo.train()          # dropout e normalização ligados
    total = 0.0
    for x, y in carregador:
        perda = perda_fn(modelo(x), y)
        otimizador.zero_grad()
        perda.backward()
        otimizador.step()
        total += perda.item() * len(y)
    return total / len(carregador.dataset)


@torch.no_grad()                # nada de grafo na avaliação
def avaliar(modelo, carregador, perda_fn):
    modelo.eval()                     # estatísticas guardadas
    perda, acertos = 0.0, 0
    for x, y in carregador:
        z = modelo(x)
        perda += perda_fn(z, y).item() * len(y)
        acertos += (z.argmax(dim=1) == y).sum().item()
    n = len(carregador.dataset)
    return perda / n, acertos / n


def salvar(caminho, modelo, otimizador, carregador, epoca):
    """Tudo o que é preciso para continuar de onde parou."""
    torch.save({"modelo": modelo.state_dict(),
                "otimizador": otimizador.state_dict(),
                "sorteador": carregador.generator.get_state(),
                "acaso": torch.get_rng_state(),  # o do dropout
                "epoca": epoca}, caminho)


def carregar(caminho, modelo, otimizador, carregador):
    estado = torch.load(caminho)
    modelo.load_state_dict(estado["modelo"])
    otimizador.load_state_dict(estado["otimizador"])
    carregador.generator.set_state(estado["sorteador"])
    torch.set_rng_state(estado["acaso"])
    return estado["epoca"]
