import torch

from folha.duas_etapas import ap_por_tipo, detecta, exemplos
from folha.duas_etapas import faster
from folha.yolo import TIPOS, Grade, MiniYolo
from folha.yolo import detecta as detecta_yolo

ancoras = torch.load("ancoras.pt")
grade = Grade("validacao", ancoras)
yolo = MiniYolo(ancoras)
yolo.load_state_dict(torch.load("yolo.pt"))
yolo.eval()
rede = faster(512)
rede.load_state_dict(torch.load("faster_512.pt"))
valid = exemplos("validacao")

dets_yolo = [detecta_yolo(yolo, grade[i][0])
             for i in range(len(grade))]
dets_faster = [detecta(rede, x) for x, _ in valid]
ap_yolo = ap_por_tipo(dets_yolo, grade.caixas)
ap_faster = ap_por_tipo(dets_faster, grade.caixas)
print("tipo             mini-YOLO  Faster R-CNN")
for t, a, b in zip(TIPOS, ap_yolo, ap_faster):
    print(f"{t:15} {a:10.3f} {b:13.3f}")
print(f"{'mAP':15} {sum(ap_yolo) / 5:10.3f}"
      f" {sum(ap_faster) / 5:13.3f}")
n_yolo = sum(p.numel() for p in yolo.parameters())
n_faster = sum(p.numel() for p in rede.parameters())
print(f"parâmetros: {n_yolo:,} contra {n_faster:,}")
