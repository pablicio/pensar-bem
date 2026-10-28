"""Parâmetros e multiplicações das arquiteturas do A2."""
import torch
from torch import nn
from torchvision import models
from torchvision.models import detection

from folha.custo import multiplicacoes, parametros
from folha.redes import lenet
from folha.unet import UNet
from folha.yolo import MiniYolo

# (núcleo, canais, passo) de cada convolução; "M", um pooling
YOLO_V1 = [(7, 64, 2), "M", (3, 192, 1), "M",
           (1, 128, 1), (3, 256, 1), (1, 256, 1), (3, 512, 1),
           "M", *[(1, 256, 1), (3, 512, 1)] * 4,
           (1, 512, 1), (3, 1024, 1), "M",
           *[(1, 512, 1), (3, 1024, 1)] * 2,
           (3, 1024, 1), (3, 1024, 2), *[(3, 1024, 1)] * 2]


def yolo_v1(S=7, B=2, C=20):
    """As 24 convoluções e as 2 densas de 2016, sem truques."""
    camadas, c = [], 3
    for item in YOLO_V1:
        if item == "M":
            camadas.append(nn.MaxPool2d(2))
            continue
        k, sai, passo = item
        camadas += [nn.Conv2d(c, sai, k, passo, k // 2),
                    nn.LeakyReLU(0.1)]
        c = sai
    return nn.Sequential(
        *camadas, nn.Flatten(), nn.Linear(S * S * 1024, 4096),
        nn.LeakyReLU(0.1),
        nn.Linear(4096, S * S * (5 * B + C)))


def dupla_valida(entrada, saida):
    return nn.Sequential(
        nn.Conv2d(entrada, saida, 3), nn.ReLU(),
        nn.Conv2d(saida, saida, 3), nn.ReLU())


class UNet2015(nn.Module):
    """A original: sem preenchimento, a foto de 572 dá 388."""

    def __init__(self, classes=2):
        super().__init__()
        c = [64, 128, 256, 512, 1024]
        self.desce = nn.ModuleList(
            [dupla_valida(e, s)
             for e, s in zip([1] + c[:3], c[:4])])
        self.fundo = dupla_valida(c[3], c[4])
        self.sobe = nn.ModuleList(
            [nn.ConvTranspose2d(c[i + 1], c[i], 2, stride=2)
             for i in (3, 2, 1, 0)])
        self.junta = nn.ModuleList(
            [dupla_valida(2 * c[i], c[i])
             for i in (3, 2, 1, 0)])
        self.saida = nn.Conv2d(c[0], classes, 1)

    def forward(self, x):
        guardados = []
        for camada in self.desce:
            x = camada(x)
            guardados.append(x)
            x = nn.functional.max_pool2d(x, 2)
        x = self.fundo(x)
        for sobe, junta, g in zip(self.sobe, self.junta,
                                  reversed(guardados)):
            x = sobe(x)
            a = (g.shape[-1] - x.shape[-1]) // 2  # o meio
            g = g[..., a:a + x.shape[-2], a:a + x.shape[-1]]
            x = junta(torch.cat([g, x], dim=1))
        return self.saida(x)


def transpostas(rede, x):
    """As multiplicações das convoluções transpostas."""
    total = 0

    def conta(camada, entrada, _):
        nonlocal total
        total += entrada[0].numel() * camada.weight[0].numel()

    ganchos = [c.register_forward_hook(conta)
               for c in rede.modules()
               if isinstance(c, nn.ConvTranspose2d)]
    with torch.no_grad():
        rede.eval()(x)
    for g in ganchos:
        g.remove()
    return total


sem = {"weights": None, "weights_backbone": None}
googlenet = models.googlenet(aux_logits=False,
                             init_weights=False)
faster = detection.fasterrcnn_resnet50_fpn(**sem)
faster_livro = detection.fasterrcnn_mobilenet_v3_large_fpn(
    num_classes=6, **sem)
REDES = [
    ("LeNet-5", lenet(), 1, 32),
    ("AlexNet", models.alexnet(), 3, 224),
    ("VGG-16", models.vgg16(), 3, 224),
    ("GoogLeNet", googlenet, 3, 224),
    ("ResNet-18", models.resnet18(), 3, 224),
    ("ResNet-50", models.resnet50(), 3, 224),
    ("MobileNetV3-S", models.mobilenet_v3_small(), 3, 224),
    ("EfficientNet-B0", models.efficientnet_b0(), 3, 224),
    ("YOLO v1", yolo_v1(), 3, 448),
    ("mini-YOLO (24)", MiniYolo(torch.ones(3, 2)), 3, 256),
    ("U-Net 2015", UNet2015(), 1, 572),
    ("U-Net (27)", UNet(), 3, 256),
    ("Faster R50-FPN", faster, 3, 0),
    ("Faster (25)", faster_livro, 3, 0)]
print(f"{'rede':16} {'entrada':>9} {'parâmetros':>12}"
      f" {'multiplicações':>16}  saída")
for nome, rede, canais, lado in REDES:
    p = parametros(rede)
    if not lado:            # o custo depende das propostas
        print(f"{nome:16} {'—':>9} {p:12,} {'—':>16}")
        continue
    x = torch.zeros(1, canais, lado, lado)
    m = multiplicacoes(rede, x) + transpostas(rede, x)
    with torch.no_grad():
        forma = "×".join(map(str, rede.eval()(x).shape[1:]))
    print(f"{nome:16} {lado:>4}×{lado:<4} {p:12,} {m:16,}"
          f"  {forma}")
