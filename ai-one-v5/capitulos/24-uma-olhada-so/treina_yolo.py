import torch

from folha.treino import fixar_semente, lotes
from folha.yolo import Grade, MiniYolo, perda

ancoras = torch.load("ancoras.pt")
fixar_semente(0, nucleos=4)
treino = Grade("treino", ancoras)
rede = MiniYolo(ancoras)
n = sum(p.numel() for p in rede.parameters())
print(f"{n:,} parâmetros")
otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
carregador = lotes(treino, 32, semente=1)
for epoca in range(1, 21):
    rede.train()
    total = 0.0
    for x, alvo in carregador:
        otimizador.zero_grad()
        p = perda(rede(x), alvo)
        p.backward()
        otimizador.step()
        total += p.item() * len(x)
    if epoca % 5 == 0:
        media = total / len(treino)
        print(f"época {epoca:2}: perda {media:.3f}")
torch.save(rede.state_dict(), "yolo.pt")
