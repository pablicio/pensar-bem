"""Autoencoders: comprimir num código e reconstruir."""
import torch
from torch import nn


class Denso(nn.Module):
    """3.072 números -> codigo -> 3.072 números."""

    def __init__(self, codigo=16, oculta=512):
        super().__init__()
        self.codificador = nn.Sequential(
            nn.Flatten(),
            nn.Linear(3 * 32 * 32, oculta), nn.ReLU(),
            nn.Linear(oculta, codigo))
        self.decodificador = nn.Sequential(
            nn.Linear(codigo, oculta), nn.ReLU(),
            nn.Linear(oculta, 3 * 32 * 32), nn.Sigmoid(),
            nn.Unflatten(1, (3, 32, 32)))

    def forward(self, x):
        return self.decodificador(self.codificador(x))


def treina(modelo, imgs, epocas=10, lote=128, alvo=None):
    """Erro quadrático entre a saída e o alvo (a própria
    entrada, se nenhum for dado); devolve a perda por época."""
    alvo = imgs if alvo is None else alvo
    otimo = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    historico = []
    for _ in range(epocas):
        total = 0.0
        for j in torch.randperm(len(imgs)).split(lote):
            perda = ((modelo(imgs[j]) - alvo[j]) ** 2).mean()
            otimo.zero_grad()
            perda.backward()
            otimo.step()
            total += perda.item() * len(j)
        historico.append(total / len(imgs))
    return historico


@torch.no_grad()
def erro(modelo, imgs):
    """O erro quadrático médio de cada imagem: (N,)."""
    return ((modelo(imgs) - imgs) ** 2).mean(dim=(1, 2, 3))
