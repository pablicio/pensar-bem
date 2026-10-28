import torch

from folha.deteccao import precisao_media
from folha.yolo import TIPOS, Grade, MiniYolo, detecta

ancoras = torch.load("ancoras.pt")
valid = Grade("validacao", ancoras)
rede = MiniYolo(ancoras)
rede.load_state_dict(torch.load("yolo.pt"))
rede.eval()
deteccoes = [detecta(rede, valid[i][0])
             for i in range(len(valid))]

print("tipo            lesões     AP  revocação máx.")
aps = []
for t, nome in enumerate(TIPOS):
    dets = [(c[k == t], n[k == t]) for c, n, k in deteccoes]
    certas = [c[c[:, 4] == t, :4] for c in valid.caixas]
    ap, _, revocacao = precisao_media(dets, certas, 0.5)
    aps.append(ap)
    n = sum(len(c) for c in certas)
    print(f"{nome:14} {n:7} {ap:6.3f} {revocacao[-1]:15.3f}")
print(f"mAP a IoU 0,5: {sum(aps) / len(aps):.3f}")

# contar pústulas de ferrugem, foto a foto
reais, contadas = [], []
for (c, n, k), certas in zip(deteccoes, valid.caixas):
    reais.append((certas[:, 4] == 0).sum().item())
    contadas.append(((k == 0) & (n > 0.3)).sum().item())
reais, contadas = torch.tensor(reais), torch.tensor(contadas)
com = reais > 0
erro = (contadas[com] - reais[com]).abs().float()
print(f"\nfotos com ferrugem: {com.sum()}; pústulas por foto:"
      f" {reais[com].float().mean():.1f}")
print(f"erro médio da contagem: {erro.mean():.2f} pústula;"
      f" contagem exata em {(erro == 0).float().mean():.0%}")
