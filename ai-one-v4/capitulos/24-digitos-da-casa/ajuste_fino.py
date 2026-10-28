from pathlib import Path

import torch
from torch import nn
from torch.utils.data import ConcatDataset, Subset

from leitora.carrega import leitora
from leitora.dados import MNIST, CaixasDoCartao
from leitora.treino import (avaliar, fixar_semente, lotes,
                            treinar_epoca)

cartoes = CaixasDoCartao("treino")
mnist = Subset(MNIST("treino"), range(10_000))
valid, teste = CaixasDoCartao("validacao"), MNIST("teste")
perda_fn = nn.CrossEntropyLoss()


def mede(modelo, nome):
    _, a = avaliar(modelo, lotes(teste, 1000), perda_fn)
    _, b = avaliar(modelo, lotes(valid, 1000), perda_fn)
    print(f"{nome:26} {a:7.2%} {b:9.2%}")


print(f"{'':26} {'MNIST':>7} {'cartões':>9}")
mede(leitora(), "antes do ajuste")
receitas = [("só cartões, taxa 1e-3", cartoes, 1e-3),
            ("só cartões, taxa 1e-4", cartoes, 1e-4),
            ("cartões + MNIST, 1e-4",
             ConcatDataset([cartoes, mnist]), 1e-4)]
for nome, dados, taxa in receitas:
    fixar_semente(0)
    modelo = leitora()              # parte da leitora do MNIST
    otimizador = torch.optim.Adam(modelo.parameters(), lr=taxa)
    carregador = lotes(dados, 64, semente=1)
    for epoca in range(5):
        treinar_epoca(modelo, carregador, otimizador, perda_fn)
    mede(modelo, nome)

Path("modelos").mkdir(exist_ok=True)
torch.save(modelo.state_dict(), "modelos/leitora_casa.pt")
