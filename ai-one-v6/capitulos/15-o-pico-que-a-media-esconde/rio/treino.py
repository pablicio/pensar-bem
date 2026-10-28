"""Exemplos, treino com parada antecipada e previsão."""
import copy

import numpy as np
import torch
from torch import nn

from rio.avalia import parte
from rio.janelas import janelas_tabela


def conjunto(tab, nivel, nome, horizontes, passado=72,
             passo=1):
    """As janelas de uma parte e as variações em cada
    horizonte, em decímetros, nas horas que têm todos eles."""
    dados, alvo = parte(tab, nome), parte(nivel, nome)
    x, _, horas = janelas_tabela(dados, alvo, passado,
                                 max(horizontes), passo)
    t = alvo.index.get_indexer(horas)
    y = alvo.to_numpy()
    y = np.stack([y[t + h] - y[t] for h in horizontes], axis=1)
    ok = ~np.isnan(y).any(axis=1)
    return (torch.tensor(x[ok], dtype=torch.float32),
            torch.tensor(10 * y[ok], dtype=torch.float32),
            horas[ok])


def preve(modelo, x, lote=4096):
    """As variações previstas, em metros."""
    modelo.eval()
    with torch.no_grad():
        partes = [modelo(x[i:i + lote])
                  for i in range(0, len(x), lote)]
    return torch.cat(partes).numpy() / 10


def treina(modelo, x, y, xv, yv, pesos=None, epocas=40,
           paciencia=4, lote=256):
    """Treina até a validação parar de melhorar; devolve o
    modelo da melhor época e o erro de validação de cada
    uma, em metros. `pesos`: quanto pesa cada exemplo."""
    otimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    melhor, guardado, historico = np.inf, None, []
    for epoca in range(epocas):
        modelo.train()
        for i in torch.randperm(len(x)).split(lote):
            quadrado = (modelo(x[i]) - y[i]) ** 2
            if pesos is not None:
                quadrado = pesos[i, None] * quadrado
            erro = quadrado.mean()
            otimizador.zero_grad()
            erro.backward()
            nn.utils.clip_grad_norm_(modelo.parameters(), 1.0)
            otimizador.step()
        validacao = float(np.abs(preve(modelo, xv) - yv.numpy()
                                 / 10).mean())
        historico.append(validacao)
        if validacao < melhor - 1e-4:
            melhor = validacao
            guardado = copy.deepcopy(modelo.state_dict())
        elif epoca - int(np.argmin(historico)) >= paciencia:
            break
    modelo.load_state_dict(guardado)
    return modelo, historico
