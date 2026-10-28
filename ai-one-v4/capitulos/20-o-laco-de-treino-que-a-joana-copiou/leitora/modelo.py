"""A rede da leitora: um módulo do PyTorch."""
from torch import nn


class MLP(nn.Module):
    """784 pixels, camadas escondidas com ReLU, 10 saídas."""

    def __init__(self, escondidas=(100,), normaliza=False,
                 dropout=0.0):
        super().__init__()
        camadas, entrada = [], 784
        for n in escondidas:
            camadas.append(nn.Linear(entrada, n))
            if normaliza:
                camadas.append(nn.BatchNorm1d(n))
            camadas.append(nn.ReLU())
            if dropout:
                camadas.append(nn.Dropout(dropout))
            entrada = n
        camadas.append(nn.Linear(entrada, 10))
        self.rede = nn.Sequential(*camadas)

    def forward(self, x):
        return self.rede(x.reshape(len(x), 784))


def conta_parametros(modelo):
    return sum(p.numel() for p in modelo.parameters())
