"""Ajuste fino da ResNet-18: taxas por camada e a sonda."""
import torch
from torch import nn

from folha.emprestada import IMAGENET_DESVIO, IMAGENET_MEDIA
from folha.emprestada import canal, extratora, treina_cabeca
from mnist import carregar


def montar():
    """A extratora com a cabeça do capítulo 16 já treinada."""
    x, y = torch.load("caracteristicas.pt")["treino"]
    rede = extratora()
    rede[1].fc = treina_cabeca(x, y)
    return rede


def por_camadas(r, taxas):
    """Um grupo do otimizador por estágio, com a sua taxa."""
    entrada = [*r.conv1.parameters(), *r.bn1.parameters()]
    estagios = [entrada + [*r.layer1.parameters()],
                r.layer2.parameters(), r.layer3.parameters(),
                r.layer4.parameters(), r.fc.parameters()]
    return [{"params": p, "lr": t}
            for p, t in zip(estagios, taxas)]


def _digitos(n=3000):
    """Dígitos do MNIST a 64 px, em três canais."""
    imagens, rotulos = carregar("treino")
    x = torch.from_numpy(imagens[:n].copy()).float() / 255
    x = nn.functional.interpolate(x[:, None], size=64,
                                  mode="bilinear")
    x = x.repeat(1, 3, 1, 1)
    x = (x - canal(IMAGENET_MEDIA)) / canal(IMAGENET_DESVIO)
    y = torch.from_numpy(rotulos[:n].astype("int64"))
    return x, y


@torch.no_grad()
def sonda(resnet):
    """Acerto de uma camada densa sobre as características da
    resnet em dígitos: quanto do que ela via ainda serve."""
    x, y = _digitos()
    fc, resnet.fc = resnet.fc, nn.Identity()
    resnet.eval()
    f = torch.cat([resnet(x[i:i + 500])
                   for i in range(0, 3000, 500)])
    resnet.fc = fc
    torch.manual_seed(0)
    densa = nn.Linear(512, 10)
    otimizador = torch.optim.Adam(densa.parameters(), lr=1e-3)
    with torch.enable_grad():
        for _ in range(300):
            otimizador.zero_grad()
            notas = densa(f[:2000])
            perda = nn.CrossEntropyLoss()(notas, y[:2000])
            perda.backward()
            otimizador.step()
    certas = densa(f[2000:]).argmax(dim=1) == y[2000:]
    return certas.float().mean().item()
