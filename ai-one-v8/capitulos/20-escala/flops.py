import torch
from torch.utils.flop_counter import FlopCounterMode

from lupa.gpt import GPT

V, T, B = 2000, 128, 4
for d, L in [(64, 2), (128, 4), (256, 6)]:
    modelo = GPT(V, T, d=d, h=4, L=L, dropout=0.0)
    x = torch.randint(0, V, (B, T))
    with FlopCounterMode(display=False) as contador:
        modelo(x, x).backward()
    medido = contador.get_total_flops() / (B * T)
    # as matrizes que multiplicam cada token: 12 d² por bloco,
    # mais a saída V x d; a atenção soma 4 T d por bloco
    N = 12 * d * d * L + V * d
    previsto = 6 * N + 3 * 4 * L * T * d
    print(f"d = {d:3}, L = {L}: medido {medido:12,.0f},"
          f" 6N + 12LTd = {previsto:12,.0f}")
