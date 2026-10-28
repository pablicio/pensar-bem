import torch
from torch import nn

from rio.avalia import erro_nos_picos, mae, parte
from rio.janelas import janelas
from rio.serie import nivel_cidade

torch.manual_seed(0)
nivel = nivel_cidade()
h = 6
x, y, _ = janelas(parte(nivel, "treino"), 24, h, passo=3)
x, y = torch.tensor(x, dtype=torch.float32), torch.tensor(y)
escala = x.std()                   # um número só, para todas
modelo = nn.Sequential(nn.Linear(24, 64), nn.ReLU(),
                       nn.Linear(64, 64), nn.ReLU(),
                       nn.Linear(64, 1))
otimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
for epoca in range(10):
    ordem = torch.randperm(len(x))
    for i in range(0, len(x), 256):
        lote = ordem[i:i + 256]
        p = modelo(x[lote] / escala).squeeze(1)
        perda = nn.functional.mse_loss(p, y[lote].float())
        otimizador.zero_grad()
        perda.backward()
        otimizador.step()
xt, yt, horas = janelas(parte(nivel, "teste"), 24, h)
with torch.no_grad():
    xt = torch.tensor(xt, dtype=torch.float32)
    p = modelo(xt / escala).squeeze(1).numpy()
picos = erro_nos_picos(nivel, p, horas, h)
print(f"MLP em {h} h: MAE {mae(p - yt) * 100:.1f} cm,"
      f" erro médio nos picos {sum(picos) / len(picos):.2f} m")
