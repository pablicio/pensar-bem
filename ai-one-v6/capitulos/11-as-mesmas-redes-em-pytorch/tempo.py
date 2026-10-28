import time
import warnings

import torch
from torch import nn

warnings.filterwarnings("ignore")
torch.manual_seed(0)
x = torch.randn(16, 50, 2)      # um lote, como o da soma


def mede(celula):
    """Milissegundos de uma ida e uma volta pela camada."""
    camada = celula(2, 16, batch_first=True)
    for _ in range(20):             # aquece
        camada(x)[0].sum().backward()
    inicio = time.perf_counter()
    for _ in range(200):
        camada(x)[0].sum().backward()
    return (time.perf_counter() - inicio) / 200 * 1000


print("              RNN    LSTM     GRU")
for nome, ligado in (("com oneDNN", True),
                     ("sem oneDNN", False)):
    with torch.backends.mkldnn.flags(enabled=ligado):
        tempos = [mede(c) for c in (nn.RNN, nn.LSTM, nn.GRU)]
    print(f"{nome}  " + "  ".join(f"{t:6.2f}" for t in tempos))
