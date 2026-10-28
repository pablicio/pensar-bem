import time

import torch

from folha.yolo import MiniYolo

torch.set_num_threads(1)          # como um celular modesto
rede = MiniYolo(torch.load("ancoras.pt"))
rede.load_state_dict(torch.load("yolo.pt"))
rede.eval()
x = torch.randn(1, 3, 256, 256)
with torch.no_grad():
    for _ in range(5):                 # aquecimento
        rede(x)
    inicio = time.perf_counter()
    for _ in range(50):
        rede(x)
tempo = (time.perf_counter() - inicio) / 50
print(f"uma foto: {tempo * 1000:.0f} ms,"
      " num núcleo do notebook")
