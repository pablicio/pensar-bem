import torch

from folha.conjunto import CLASSES
from folha.fundos import TIPOS, FundoTrocado
from folha.redes import rede_global
from folha.treino import lotes, prever

FERRUGEM = CLASSES.index("ferrugem")
SADIA = CLASSES.index("sadia")
fotos = {tipo: FundoTrocado("validacao", tipo)
         for tipo in TIPOS}
print("rede          fundo     acerto  sadia  viram ferrugem")
for nome in ("sempre", "matiz", "matiz_fundos"):
    rede = rede_global()
    rede.load_state_dict(torch.load(f"{nome}.pt"))
    for tipo in TIPOS:
        prevista, certa = prever(rede, lotes(fotos[tipo], 256))
        sadias = prevista[certa == SADIA]
        sadia = (sadias == SADIA).float().mean()
        acerto = (prevista == certa).float().mean()
        ferrugem = (prevista == FERRUGEM).sum()
        print(f"{nome:13} {tipo:8} {acerto:7.1%} {sadia:6.0%}"
              f" {ferrugem:7} de {len(certa)}")
