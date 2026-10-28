import torch

from folha.caixas import iou
from folha.localizacao import Lesoes, RedeLocal, perda
from folha.treino import fixar_semente, lotes

print("alvo   lesões  fotos  IoU média  IoU > 0,5  classe")
for alvo in ("maior", "uniao"):
    treino = Lesoes("treino", alvo)
    valid = Lesoes("validacao", alvo)
    fixar_semente(0, nucleos=4)
    rede = RedeLocal()
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 64, semente=1)
    for epoca in range(30):
        rede.train()
        for x, y, caixa, tem in carregador:
            otimizador.zero_grad()
            perda(rede(x), y, caixa, tem).backward()
            otimizador.step()
    rede.eval()
    with torch.no_grad():
        x = torch.stack([valid[i][0]
                         for i in range(len(valid))])
        notas, caixas = rede(x)
    certa = valid.fotos.rotulos
    acerto = (notas.argmax(dim=1) == certa).float().mean()
    tem = valid.quantas > 0
    sobre = iou(caixas[tem], valid.caixas[tem]).diagonal()
    n = valid.quantas[tem]
    grupos = [("1", n == 1), ("2 a 3", (n >= 2) & (n <= 3)),
              ("4 ou +", n >= 4), ("todas", n > 0)]
    for nome, grupo in grupos:
        s = sobre[grupo]
        boas = (s > 0.5).float().mean()
        print(f"{alvo:6} {nome:7} {len(s):5} {s.mean():10.3f}"
              f" {boas:10.1%} {acerto:7.1%}")
    torch.save(rede.state_dict(), f"local_{alvo}.pt")
