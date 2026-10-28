import numpy as np
import torch
from torch import nn

from rio.numpy_lstm import lstm, lstm_inicia
from rio.numpy_treino import tarefa_soma

S = 16
p = lstm_inicia(2, S, np.random.default_rng(1))
xs, _ = tarefa_soma(np.random.default_rng(0), 3, 50)

camada = nn.LSTM(input_size=2, hidden_size=S, batch_first=True)
# o livro: entrada, esquecimento, saída, candidato
# o PyTorch: entrada, esquecimento, candidato, saída
ordem = np.r_[0:2 * S, 3 * S:4 * S, 2 * S:3 * S]
W, b = p["W"][ordem], p["b"][ordem]
with torch.no_grad():
    camada.weight_ih_l0.copy_(torch.tensor(W[:, :2]))
    camada.weight_hh_l0.copy_(torch.tensor(W[:, 2:]))
    camada.bias_ih_l0.copy_(torch.tensor(b))
    camada.bias_hh_l0.zero_()
    lote = torch.tensor(xs, dtype=torch.float32)
    _, (h_torch, c_torch) = camada(lote)
for k in range(3):
    _, h, c = lstm(p, xs[k])
    dif_h = np.abs(h - h_torch[0, k].numpy()).max()
    dif_c = np.abs(c - c_torch[0, k].numpy()).max()
    print(f"sequência {k}: diferença em h {dif_h:.1e},"
          f" em c {dif_c:.1e}")
