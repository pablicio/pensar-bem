import time

import torch

from lauber.anomalia import Malha, escores, mapa_de_erro

torch.set_num_threads(1)              # um núcleo por câmera
rede = Malha()
rede.load_state_dict(torch.load("malha.pt"))
rede.eval()
for lote in (1, 4, 32):
    fotos = torch.rand(lote, 1, 32, 32)
    escores(mapa_de_erro(rede, fotos))     # aquece
    inicio, vezes = time.perf_counter(), 200
    for _ in range(vezes):
        escores(mapa_de_erro(rede, fotos))
    por_foto = (time.perf_counter() - inicio) / (vezes * lote)
    ms = por_foto * 1000
    print(f"lotes de {lote:2d}: {1 / por_foto:6.0f} fotos por"
          f" segundo num núcleo ({ms:.2f} ms cada)")
precisa = 46 * 4
print(f"46 teares x 4 fotos por segundo = {precisa} fotos por"
      " segundo")
