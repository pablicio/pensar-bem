"""Um Transformer de imagens e uma rede convolucional."""
import torch
from torch import nn

from .bloco import Bloco


class ViT(nn.Module):
    """A imagem em pedaços p x p, cada pedaço um token."""

    def __init__(self, lado=32, p=8, d=64, h=4, L=2,
                 classes=10):
        super().__init__()
        n = (lado // p) ** 2                      # 16 pedaços
        self.pedacos = nn.Conv2d(1, d, kernel_size=p, stride=p)
        self.classe = nn.Parameter(torch.zeros(1, 1, d))
        pos = 0.02 * torch.randn(1, n + 1, d)
        self.pos = nn.Parameter(pos)
        self.blocos = nn.ModuleList(Bloco(d, h)
                                    for _ in range(L))
        self.norma = nn.LayerNorm(d)
        self.cabeca = nn.Linear(d, classes)

    def forward(self, x):
        # (B, d, 4, 4) -> (B, 16, d): um token por pedaço
        t = self.pedacos(x).flatten(2).transpose(1, 2)
        classe = self.classe.expand(len(x), -1, -1)
        h = torch.cat([classe, t], dim=1) + self.pos
        for b in self.blocos:
            h = b(h)                              # sem máscara
        return self.cabeca(self.norma(h[:, 0]))   # o [CLS]


def CNN(classes=10):
    """Duas convoluções 3 x 3 com redução, como no volume 5."""
    return nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(), nn.Linear(32 * 8 * 8, 64), nn.ReLU(),
        nn.Linear(64, classes))
