import torch

from folha.duas_etapas import ajusta, ap_por_tipo, detecta
from folha.duas_etapas import exemplos, faster
from folha.treino import fixar_semente
from folha.yolo import TIPOS

treino, valid = exemplos("treino"), exemplos("validacao")
certas = [torch.cat([a["boxes"], a["labels"][:, None] - 1], 1)
          for _, a in valid]
for lado in (256, 512):
    print(f"--- fotos redimensionadas para {lado} pixels")
    fixar_semente(0, nucleos=4)
    rede = faster(lado)
    ajusta(rede, treino, epocas=2)
    deteccoes = [detecta(rede, x) for x, _ in valid]
    aps = ap_por_tipo(deteccoes, certas)
    print("  ".join(f"{t[:5]} {a:.3f}"
                    for t, a in zip(TIPOS, aps)))
    print(f"mAP a IoU 0,5: {sum(aps) / len(aps):.3f}")
    torch.save(rede.state_dict(), f"faster_{lado}.pt")
