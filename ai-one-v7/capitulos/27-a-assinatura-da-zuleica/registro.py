import json

import torch

from lauber.acervo import carrega, partes
from lauber.dcgan import CODIGO, desenha
from lauber.emenda import GeradorCircular, costura
from lauber.procedencia import (grava, impressao, parecidas,
                                registro)
from lauber.serigrafia import delta_e, reduz

imgs, info = carrega()
treino, _, _ = partes(len(imgs))
da_zuleica = info["zuleica"][treino].mean()
print(f"estampas da Zuleica no treino: {da_zuleica:.0%}")
gerador = GeradorCircular()
gerador.load_state_dict(torch.load("emenda.pt"))
maquina = {"gerador": "GeradorCircular, capítulo 25",
           "pesos": impressao("emenda.pt"),
           "dados": impressao("dados/brutos/acervo.npz")}

registros = []
for numero, semente in enumerate((11, 12, 13, 14), start=1):
    torch.manual_seed(semente)
    x = desenha(gerador, torch.randn(1, CODIGO))
    img = x[0].permute(1, 2, 0).numpy().astype(float)
    rotulos, paleta = reduz(img, 6)
    verificacoes = {
        "costura": round(costura(x), 2),
        "delta_e_seis_cores": round(
            delta_e(img, paleta[rotulos]), 1)}
    vizinhas = parecidas(x, imgs[treino], info, treino)
    desta = maquina | {"semente": semente}
    registros.append(registro(numero, desta, verificacoes,
                              vizinhas))
grava(registros, "registro.jsonl")
print(json.dumps(registros[0], ensure_ascii=False, indent=1))
zuleica = sum(v["zuleica"] for r in registros
              for v in r["parecidas_no_acervo"])
print(f"das 12 mais parecidas das 4 estampas,"
      f" {zuleica} são da Zuleica")
