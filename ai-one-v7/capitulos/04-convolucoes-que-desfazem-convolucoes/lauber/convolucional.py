"""O autoencoder convolucional: o código é uma imagem menor."""
from torch import nn


def sobe(entrada, saida, tipo):
    """Dobra a altura e a largura."""
    if tipo == "transposta":
        return nn.ConvTranspose2d(entrada, saida, 3, stride=2,
                                  padding=1, output_padding=1)
    # reamostra: repete cada pixel em 2 x 2 e convolui
    return nn.Sequential(
        nn.Upsample(scale_factor=2),
        nn.Conv2d(entrada, saida, 3, padding=1))


class Convolucional(nn.Module):
    """32 x 32 x 3 -> código 8 x 8 x canais -> 32 x 32 x 3."""

    def __init__(self, tipo="reamostra", canais=4):
        super().__init__()
        self.codificador = nn.Sequential(
            nn.Conv2d(3, 32, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, canais, 3, padding=1))
        self.decodificador = nn.Sequential(
            nn.Conv2d(canais, 64, 3, padding=1), nn.ReLU(),
            sobe(64, 32, tipo), nn.ReLU(),
            sobe(32, 3, tipo), nn.Sigmoid())

    def forward(self, x):
        return self.decodificador(self.codificador(x))
