import time

import torch

from folha.duas_etapas import faster
from folha.yolo import MiniYolo

torch.set_num_threads(1)
foto = torch.rand(3, 256, 256)
yolo = MiniYolo(torch.load("ancoras.pt")).eval()
rede = faster(512).eval()


def mede(funcao, vezes=20):
    with torch.no_grad():
        for _ in range(3):
            funcao()
        inicio = time.perf_counter()
        for _ in range(vezes):
            funcao()
    return (time.perf_counter() - inicio) / vezes * 1000


um = mede(lambda: yolo(foto[None]))
dois = mede(lambda: rede([foto]))
print(f"mini-YOLO:    {um:5.0f} ms")
print(f"Faster R-CNN: {dois:5.0f} ms")
