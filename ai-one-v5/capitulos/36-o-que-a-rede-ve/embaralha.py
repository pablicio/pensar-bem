import torch
from torch.utils.data import TensorDataset

from folha.conjunto import Folhas
from folha.emprestada import extrai, extratora, treina_cabeca
from folha.treino import fixar_semente

fixar_semente(0, nucleos=4)
xt, yt = torch.load("caracteristicas.pt")["treino"]
cabeca = treina_cabeca(xt, yt)
resnet = extratora()
valid = Folhas("validacao")
x = torch.stack([valid[i][0] for i in range(len(valid))])
sorteador = torch.Generator().manual_seed(36)


def embaralha(x, g):
    """Corta cada foto em g × g pedaços e os sorteia."""
    n, c, h, w = x.shape
    p = h // g
    pedacos = x.unfold(2, p, p).unfold(3, p, p)   # N×C×g×g×p×p
    pedacos = pedacos.reshape(n, c, g * g, p, p)
    ordem = torch.randperm(g * g, generator=sorteador)
    pedacos = pedacos[:, :, ordem].reshape(n, c, g, g, p, p)
    pedacos = pedacos.permute(0, 1, 2, 4, 3, 5)
    return pedacos.reshape(n, c, h, w)


print("grade   pedaço   acerto")
for g in (1, 2, 4, 8, 16):
    f, _ = extrai(resnet, TensorDataset(embaralha(x, g),
                                        valid.rotulos))
    acerto = (cabeca(f).argmax(dim=1) == valid.rotulos).float()
    print(f"{g:2}×{g:<2} {128 // g:5} px {acerto.mean():8.1%}")
