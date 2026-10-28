"""Espinhas dorsais da ImageNet, leves e pesadas."""
from torch import nn
from torchvision.models import (
    EfficientNet_B0_Weights, MobileNet_V3_Small_Weights,
    ResNet18_Weights, efficientnet_b0, mobilenet_v3_small,
    resnet18)

from folha.emprestada import Renormaliza


def espinha(nome):
    """(rede: foto → características, quantas são)."""
    if nome == "ResNet-18":
        rede = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        rede.fc = nn.Identity()
        n = 512
    elif nome == "MobileNetV3-S":
        pesos = MobileNet_V3_Small_Weights.IMAGENET1K_V1
        rede = mobilenet_v3_small(weights=pesos)
        rede.classifier = nn.Identity()
        n = 576
    else:
        pesos = EfficientNet_B0_Weights.IMAGENET1K_V1
        rede = efficientnet_b0(weights=pesos)
        rede.classifier = nn.Identity()
        n = 1280
    return nn.Sequential(Renormaliza(), rede).eval(), n


ESPINHAS = ("ResNet-18", "MobileNetV3-S", "EfficientNet-B0")
