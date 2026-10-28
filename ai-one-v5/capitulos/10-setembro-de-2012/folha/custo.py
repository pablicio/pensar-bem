"""Parâmetros e multiplicações de uma rede, camada a camada."""
import torch
from torch import nn


def multiplicacoes(rede, entrada):
    """Soma S·C·k²·H'·W' das convoluções e n·m das densas."""
    total = 0

    def conta(camada, _, saida):
        nonlocal total
        if isinstance(camada, nn.Conv2d):
            k = camada.weight[0].numel()   # C·k² por saída
            total += saida.numel() * k
        elif isinstance(camada, nn.Linear):
            total += camada.in_features * camada.out_features

    ganchos = [c.register_forward_hook(conta)
               for c in rede.modules()
               if isinstance(c, (nn.Conv2d, nn.Linear))]
    with torch.no_grad():
        rede.eval()(entrada)
    for g in ganchos:
        g.remove()
    return total


def parametros(rede):
    return sum(p.numel() for p in rede.parameters())
