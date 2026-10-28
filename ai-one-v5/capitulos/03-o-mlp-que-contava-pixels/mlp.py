from pathlib import Path

import torch
from torch import nn

from folha.conjunto import Folhas
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca

fixar_semente(0)
treino, valid = Folhas("treino"), Folhas("validacao")
mlp = nn.Sequential(nn.Flatten(),
                    nn.Linear(3 * 128 * 128, 256), nn.ReLU(),
                    nn.Linear(256, 6))
for nome, p in mlp.named_parameters():
    formato = str(tuple(p.shape))
    print(f"{nome:9} {formato:13} {p.numel():>11,}")
total = sum(p.numel() for p in mlp.parameters())
print(f"{'total':23} {total:>11,}\n")

otimizador = torch.optim.Adam(mlp.parameters(), lr=1e-4)
carregador = lotes(treino, 64, semente=1)
for epoca in range(1, 11):
    perda = treinar_epoca(mlp, carregador, otimizador,
                          nn.CrossEntropyLoss())
    if epoca % 3 == 0 or epoca == 10:
        acerto = acuracia(mlp, lotes(valid, 256))
        print(f"época {epoca:2}: perda {perda:.3f},"
              f" validação {acerto:.1%}")
Path("modelos").mkdir(exist_ok=True)
torch.save(mlp.state_dict(), "modelos/mlp.pt")
