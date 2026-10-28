"""A leitora treinada, pronta para ler."""
import torch

from leitora.modelo import MLP

ARQUITETURA = {"escondidas": (256, 128), "normaliza": True,
               "dropout": 0.2}


def leitora(caminho="modelos/leitora_mnist.pt"):
    modelo = MLP(**ARQUITETURA)
    modelo.load_state_dict(torch.load(caminho))
    return modelo.eval()               # pronta para avaliar


@torch.no_grad()
def probabilidades(modelo, imagens):
    return torch.softmax(modelo(imagens), dim=1)
