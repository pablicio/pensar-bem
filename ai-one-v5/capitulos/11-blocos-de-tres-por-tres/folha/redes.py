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


def lenet(canais=1, classes=10):
    """A LeNet-5 de 1998, com as simplificações de hoje."""
    return nn.Sequential(
        nn.Conv2d(canais, 6, 5), nn.Tanh(),      # C1: 6 × 28²
        nn.AvgPool2d(2),                         # S2: 6 × 14²
        nn.Conv2d(6, 16, 5), nn.Tanh(),          # C3: 16 × 10²
        nn.AvgPool2d(2),                         # S4: 16 × 5²
        nn.Conv2d(16, 120, 5), nn.Tanh(),        # C5: 120 × 1²
        nn.Flatten(),
        nn.Linear(120, 84), nn.Tanh(),           # F6
        nn.Linear(84, classes))                  # saída


def vgg(convs_por_bloco, larguras=(16, 32, 64, 128)):
    """Blocos de convoluções 3×3 e um max pooling, à la VGG."""
    camadas, canais = [], 3
    for largura in larguras:
        for _ in range(convs_por_bloco):
            conv = nn.Conv2d(canais, largura, 3, padding=1)
            camadas += [conv, nn.ReLU()]
            canais = largura
        camadas.append(nn.MaxPool2d(2))
    return nn.Sequential(*camadas, nn.AdaptiveAvgPool2d(1),
                         nn.Flatten(), nn.Linear(canais, 6))
