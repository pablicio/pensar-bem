"""Convoluções causais dilatadas sobre a série do rio."""
import torch
import torch.nn.functional as F
from torch import nn


class Convolucional(nn.Module):
    """Convoluções 1D com dilatação 1, 2, 4, ...: cada hora
    vê só ela e as anteriores, até o alcance da rede."""

    def __init__(self, entradas, horizontes, canais=32,
                 dilatacoes=(1, 2, 4, 8, 16), k=3):
        super().__init__()
        self.k = k
        self.entrada = nn.Conv1d(entradas, canais, 1)
        self.camadas = nn.ModuleList(
            nn.Conv1d(canais, canais, k, dilation=d)
            for d in dilatacoes)
        self.saida = nn.Linear(canais, len(horizontes))
        self.alcance = 1 + (k - 1) * sum(dilatacoes)

    def por_hora(self, x):
        """(lote, horas, colunas) -> as previsões de todas as
        horas, (lote, horas, horizontes)."""
        z = self.entrada(x.transpose(1, 2))
        for conv in self.camadas:
            atras = (self.k - 1) * conv.dilation[0]
            z = z + torch.relu(conv(F.pad(z, (atras, 0))))
        return self.saida(z.transpose(1, 2))

    def forward(self, x):
        return self.por_hora(x)[:, -1]
