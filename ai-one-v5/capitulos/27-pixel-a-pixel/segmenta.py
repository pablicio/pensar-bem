import torch
from torch import nn

from folha.treino import fixar_semente, lotes
from folha.unet import CLASSES_PIXEL, Mascaras, UNet
from folha.unet import dice_suave, medidas

treino, valid = Mascaras("treino"), Mascaras("validacao")
print("pixels de cada classe no treino:",
      (torch.bincount(treino.mascaras.flatten()) /
       treino.mascaras.numel()).numpy().round(4))
for atalhos in (False, True):
    fixar_semente(0, nucleos=4)
    rede = UNet(atalhos=atalhos)
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 16, semente=1)
    for epoca in range(8):
        rede.train()
        for x, m in carregador:
            otimizador.zero_grad()
            notas = rede(x)
            perda = nn.functional.cross_entropy(notas, m) \
                + dice_suave(notas, m)
            perda.backward()
            otimizador.step()
    rede.eval()
    with torch.no_grad():
        prevista = torch.cat([rede(x).argmax(dim=1)
                              for x, _ in lotes(valid, 32)])
    dice, iou = medidas(prevista, valid.mascaras)
    nome = "U-Net" if atalhos else "sem atalhos"
    n = sum(p.numel() for p in rede.parameters())
    print(f"\n{nome}: {n:,} parâmetros")
    for c, d, i in zip(CLASSES_PIXEL, dice, iou):
        print(f"  {c:6} Dice {d:.3f}  IoU {i:.3f}")
    torch.save(rede.state_dict(),
               "unet.pt" if atalhos else "sem_atalhos.pt")
