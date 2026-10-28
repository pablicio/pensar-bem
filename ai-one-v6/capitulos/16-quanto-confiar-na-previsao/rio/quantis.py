"""Previsão por quantis: a perda pinball e o treino."""
import copy

import numpy as np
import torch
from torch import nn

QUANTIS = torch.tensor([0.05, 0.5, 0.95])


def pinball(previsto, alvo):
    """previsto: (lote, horizontes, quantis); alvo: (lote,
    horizontes). Pune mais o lado errado de cada quantil."""
    erro = alvo[:, :, None] - previsto
    return torch.maximum(QUANTIS * erro, (QUANTIS - 1) * erro)


def preve_quantis(modelo, x, lote=4096):
    """(exemplos, horizontes, quantis), em metros, em ordem."""
    modelo.eval()
    with torch.no_grad():
        p = torch.cat([modelo(x[i:i + lote])
                       for i in range(0, len(x), lote)])
    p = p.view(len(x), -1, len(QUANTIS)) / 10
    return torch.sort(p, dim=2).values.numpy()


def treina_quantis(modelo, x, y, xv, yv, epocas=40,
                   paciencia=4, lote=256):
    """O treino do capítulo 13, com a perda pinball."""
    otimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    historico, melhor = [], None
    q = len(QUANTIS)
    for epoca in range(epocas):
        modelo.train()
        for i in torch.randperm(len(x)).split(lote):
            p = modelo(x[i]).view(len(i), -1, q)
            erro = pinball(p, y[i]).mean()
            otimizador.zero_grad()
            erro.backward()
            nn.utils.clip_grad_norm_(modelo.parameters(), 1.0)
            otimizador.step()
        pv = torch.tensor(preve_quantis(modelo, xv) * 10)
        historico.append(float(pinball(pv, yv).mean()))
        if historico[-1] == min(historico):
            melhor = copy.deepcopy(modelo.state_dict())
        elif epoca - int(np.argmin(historico)) >= paciencia:
            break
    modelo.load_state_dict(melhor)
    return modelo, historico
