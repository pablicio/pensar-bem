"""Para onde a rede olha: o Grad-CAM, à mão."""
import torch
from torch import nn


def gradcam(rede, camada, x, classe=None):
    """O mapa de cada foto do lote x, de 0 a 1, no tamanho da
    foto. Sem `classe`, explica a que a rede escolheu."""
    guardado = {}

    def na_ida(modulo, entrada, saida):
        guardado["A"] = saida
        saida.register_hook(lambda g: guardado.update(G=g))

    gancho = camada.register_forward_hook(na_ida)
    rede.eval()
    notas = rede(x)
    gancho.remove()
    if classe is None:
        classe = notas.argmax(dim=1)
    rede.zero_grad()
    notas[torch.arange(len(x)), classe].sum().backward()
    A, G = guardado["A"], guardado["G"]        # N × K × h × w
    alfa = G.mean(dim=(2, 3), keepdim=True)     # N × K × 1 × 1
    mapa = torch.relu((alfa * A).sum(dim=1))    # N × h × w
    mapa = nn.functional.interpolate(mapa[:, None],
                                     size=x.shape[-2:],
                                     mode="bilinear")[:, 0]
    maior = mapa.flatten(1).max(dim=1).values
    return (mapa / (maior.view(-1, 1, 1) + 1e-8)).detach()
