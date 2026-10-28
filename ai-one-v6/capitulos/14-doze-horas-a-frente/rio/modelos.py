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


class EncoderDecoder(nn.Module):
    """Uma LSTM lê a janela; outra, começando do estado dela,
    escreve uma hora de cada vez, recebendo a hora anterior."""

    def __init__(self, entradas, passos, estado=64):
        super().__init__()
        self.passos = passos
        self.leitor = nn.LSTM(entradas, estado,
                              batch_first=True)
        self.escritor = nn.LSTM(1, estado, batch_first=True)
        self.saida = nn.Linear(estado, 1)

    def forward(self, x, alvo=None):
        _, estado = self.leitor(x)
        anterior = torch.zeros(len(x), 1, 1)
        saidas = []
        for k in range(self.passos):
            h, estado = self.escritor(anterior, estado)
            prevista = self.saida(h)            # (lote, 1, 1)
            saidas.append(prevista)
            if alvo is not None:          # teacher forcing
                anterior = alvo[:, k].view(-1, 1, 1)
            else:
                anterior = prevista
        return torch.cat(saidas, dim=1).squeeze(2)
