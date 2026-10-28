"""Uma rede recorrente que lê mensagens e diz a classe."""
import numpy as np
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence

from rio.texto import CLASSES


def preenche(voc, textos, maximo=60):
    """Matriz (mensagens, maximo) de números, completada com 0,
    e o tamanho de cada mensagem."""
    ids = [voc.codifica(t)[:maximo] or [1] for t in textos]
    x = torch.zeros(len(ids), maximo, dtype=torch.long)
    for i, seq in enumerate(ids):
        x[i, :len(seq)] = torch.tensor(seq)
    return x, torch.tensor([len(s) for s in ids])


class Leitor(nn.Module):
    def __init__(self, n_palavras, dim=32, estado=64,
                 bidirecional=False, camadas=1, dropout=0.0):
        super().__init__()
        self.emb = nn.Embedding(n_palavras, dim, padding_idx=0)
        self.lstm = nn.LSTM(dim, estado, num_layers=camadas,
                            batch_first=True, dropout=dropout,
                            bidirectional=bidirecional)
        lados = 2 if bidirecional else 1
        self.saida = nn.Linear(lados * estado, len(CLASSES))

    def forward(self, x, n):
        pacote = pack_padded_sequence(self.emb(x), n,
                                      batch_first=True,
                                      enforce_sorted=False)
        _, (h, _) = self.lstm(pacote)
        if self.lstm.bidirectional:
            ultimo = torch.cat([h[-2], h[-1]], dim=1)
        else:
            ultimo = h[-1]
        return self.saida(ultimo)


def treina_leitor(modelo, dados, validacao, epocas=30,
                  paciencia=4, lote=64):
    """Adam, parada antecipada pela perda de validação."""
    x, n, y = dados
    xv, nv, yv = validacao
    otimo = torch.optim.Adam(modelo.parameters(), lr=2e-3)
    perda_fn = nn.CrossEntropyLoss()
    melhor, estado, espera = np.inf, None, 0
    for epoca in range(epocas):
        modelo.train()
        for j in torch.randperm(len(y)).split(lote):
            perda = perda_fn(modelo(x[j], n[j]), y[j])
            otimo.zero_grad()
            perda.backward()
            otimo.step()
        modelo.eval()
        with torch.no_grad():
            pv = perda_fn(modelo(xv, nv), yv).item()
        if pv < melhor:
            melhor, espera = pv, 0
            estado = {k: v.clone()
                      for k, v in modelo.state_dict().items()}
        else:
            espera += 1
            if espera == paciencia:
                break
    modelo.load_state_dict(estado)
    return epoca + 1, melhor


def probabilidades(modelo, x, n):
    modelo.eval()
    with torch.no_grad():
        return torch.softmax(modelo(x, n), dim=1).numpy()
