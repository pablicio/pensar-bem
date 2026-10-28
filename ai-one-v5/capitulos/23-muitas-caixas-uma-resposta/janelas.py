import torch

from folha.deteccao import Janelas, perda, rede_janelas
from folha.treino import fixar_semente, lotes

fixar_semente(0, nucleos=4)
treino = Janelas("treino")
rede = rede_janelas()
otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
carregador = lotes(treino, 32, semente=1)
for epoca in range(1, 16):
    rede.train()
    total = 0.0
    for x, alvo, desloc in carregador:
        otimizador.zero_grad()
        p = perda(rede(x), alvo, desloc)
        p.backward()
        otimizador.step()
        total += p.item() * len(x)
    if epoca % 5 == 0:
        media = total / len(treino)
        print(f"época {epoca:2}: perda {media:.4f}")
torch.save(rede.state_dict(), "janelas.pt")
