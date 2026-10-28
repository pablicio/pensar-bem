import torch
from torch import nn

torch.manual_seed(0)
lstm = nn.LSTM(input_size=2, hidden_size=16, batch_first=True)
x = torch.randn(64, 50, 2)          # lote, horas, entradas
saida, (h, c) = lstm(x)
print("entrada  ", tuple(x.shape))
print("saída    ", tuple(saida.shape))
print("h e c    ", tuple(h.shape), tuple(c.shape))
print("o último h é a última saída:",
      torch.equal(saida[:, -1], h[0]))
for nome, peso in lstm.named_parameters():
    print(f"{nome:14} {tuple(peso.shape)}")
