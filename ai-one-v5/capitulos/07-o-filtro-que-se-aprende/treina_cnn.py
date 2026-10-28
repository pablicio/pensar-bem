from pathlib import Path

import torch
from torch import nn

from folha.conjunto import Folhas
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca

fixar_semente(0)
treino, valid = Folhas("treino"), Folhas("validacao")
rede = nn.Sequential(
    nn.Conv2d(3, 16, 5, stride=2, padding=2), nn.ReLU(),
    nn.Conv2d(16, 32, 3, stride=2, padding=1), nn.ReLU(),
    nn.Conv2d(32, 64, 3, stride=2, padding=1), nn.ReLU(),
    nn.Flatten(), nn.Linear(64 * 16 * 16, 6))
for nome, p in rede.named_parameters():
    if nome.endswith("weight"):
        formato = str(tuple(p.shape))
        print(f"{nome:9} {formato:18} {p.numel():>7,}")
total = sum(p.numel() for p in rede.parameters())
print(f"total, com os vieses: {total:,}\n")

otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
carregador = lotes(treino, 64, semente=1)
for epoca in range(1, 11):
    perda = treinar_epoca(rede, carregador, otimizador,
                          nn.CrossEntropyLoss())
    if epoca % 3 == 0 or epoca == 10:
        acerto = acuracia(rede, lotes(valid, 256))
        print(f"época {epoca:2}: perda {perda:.3f},"
              f" validação {acerto:.1%}")
Path("modelos").mkdir(exist_ok=True)
torch.save(rede.state_dict(), "modelos/cnn.pt")
