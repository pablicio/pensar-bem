"""As redes do livro, das mais simples às mais profundas."""
from torch import nn


def bloco_pool(entrada, saida):
    """Convolução 3×3, ReLU e max pooling 2×2."""
    return [nn.Conv2d(entrada, saida, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2)]


def rede_densa():
    """Três blocos e uma camada densa: 128 → 16 pixels."""
    return nn.Sequential(
        *bloco_pool(3, 16), *bloco_pool(16, 32),
        *bloco_pool(32, 64), nn.Flatten(),
        nn.Linear(64 * 16 * 16, 6))


def rede_global():
    """Quatro blocos e a média de cada canal no fim."""
    return nn.Sequential(
        *bloco_pool(3, 16), *bloco_pool(16, 32),
        *bloco_pool(32, 64), *bloco_pool(64, 64),
        nn.AdaptiveAvgPool2d(1), nn.Flatten(),
        nn.Linear(64, 6))
