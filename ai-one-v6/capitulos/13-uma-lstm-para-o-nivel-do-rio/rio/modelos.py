"""As redes que preveem o rio."""
import torch
from torch import nn


class Previsor(nn.Module):
    """Uma LSTM lê a janela; uma camada linear prevê a variação
    do nível em cada horizonte, a partir do último estado."""

    def __init__(self, entradas, horizontes, estado=32):
        super().__init__()
        self.lstm = nn.LSTM(entradas, estado, batch_first=True)
        self.saida = nn.Linear(estado, len(horizontes))

    def forward(self, x):
        estados, _ = self.lstm(x)
        return self.saida(estados[:, -1])
