import time

import torch
from torch import nn

torch.manual_seed(0)
LOTE, DIM = 32, 64
lstm = nn.LSTM(DIM, DIM, batch_first=True)
conv = nn.Sequential(*[nn.Conv1d(DIM, DIM, 3, padding="same",
                                 dilation=2 ** i)
                       for i in range(5)])
atencao = nn.MultiheadAttention(DIM, 4, batch_first=True)


def mede(funcao, x, vezes=3):
    with torch.no_grad():
        funcao(x)                         # aquece
        inicio = time.perf_counter()
        for _ in range(vezes):
            funcao(x)
    return (time.perf_counter() - inicio) / vezes * 1000


print("passos     LSTM   convolução   atenção   (ms por lote)")
for passos in (64, 256, 1024, 4096):
    x = torch.randn(LOTE, passos, DIM)
    t_lstm = mede(lambda z: lstm(z), x)
    t_conv = mede(lambda z: conv(z.transpose(1, 2)), x)
    t_aten = mede(lambda z: atencao(z, z, z,
                                    need_weights=False), x)
    print(f"{passos:6d} {t_lstm:8.1f} {t_conv:12.1f}"
          f" {t_aten:9.1f}")
