import torch
from torch import nn

from folha.pontos import GiradasPontos, Mapas, Pontos
from folha.pontos import Regressao, angulo
from folha.treino import fixar_semente, lotes

treino = Pontos("treino", gira=True)
testes = {q: GiradasPontos(q) for q in ("em_pe", "girada")}
print("rede       fotos   ponta  pecíolo  ângulo: mediana"
      "  > 20°")
for nome, Rede in (("regressão", Regressao), ("mapas", Mapas)):
    fixar_semente(0, nucleos=4)
    rede = Rede()
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 64, semente=1)
    for epoca in range(30):
        rede.train()
        for x, p in carregador:
            otimizador.zero_grad()
            nn.functional.l1_loss(rede(x), p).backward()
            otimizador.step()
    rede.eval()
    for qual, teste in testes.items():
        with torch.no_grad():
            previstos = rede(teste.x) * 128
        erro = (previstos - teste.pontos).norm(dim=2)  # pixels
        giro = angulo(previstos) - angulo(teste.pontos)
        giro = (giro + 180) % 360 - 180    # de -180 a 180
        ponta, peciolo = erro.mean(dim=0)
        mediana = giro.abs().median()
        longe = (giro.abs() > 20).float().mean()
        print(f"{nome:10} {qual:6} {ponta:5.1f} px"
              f" {peciolo:5.1f} px {mediana:9.1f}°"
              f" {longe:8.1%}")
    torch.save(rede.state_dict(), f"pontos_{nome}.pt")
