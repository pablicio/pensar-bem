import csv

import torch
import torch.nn.functional as F

from lupa.cnpj import FORMATO, valido
from lupa.corpus import prepara
from lupa.diario import BRUTOS
from lupa.escolha import amostra, gulosa
from lupa.gpt import GPT

tok, treino, teste = prepara()
modelo = GPT(len(tok.vocab))
modelo.load_state_dict(torch.load("gpt.pt"))
modelo.eval()
with open(BRUTOS / "empresas.csv", encoding="utf-8") as f:
    lista = {e["cnpj"] for e in csv.DictReader(f)}
print(f"{len(lista)} CNPJs na lista, válidos:"
      f" {sum(map(valido, lista))}")

# cada "CNPJ nº" de 2027, com os 100 tokens anteriores
chave = tok.codifica(" CNPJ nº")
pos = [i for i in range(100, len(teste) - 20)
       if teste[i - 1:i + 1].tolist() == chave]
contexto = torch.stack([teste[i - 99:i + 1] for i in pos])
certo = [tok.decodifica(teste[i + 1:i + 19].tolist()).strip()
         for i in pos]
print(f"{len(pos)} CNPJs em 2027")

g = torch.Generator().manual_seed(0)
for nome, escolhe in [("gulosa", gulosa),
                      ("T = 1", amostra(1.0, gerador=g))]:
    ids = modelo.gera(contexto, 18, escolhe)[:, -18:]
    escritos = [tok.decodifica(s).strip()
                for s in ids.tolist()]
    ok = [FORMATO.fullmatch(c) is not None for c in escritos]
    igual = sum(c == v for c, v in zip(escritos, certo))
    outro = sum(c in lista and c != v
                for c, v in zip(escritos, certo))
    novos = [c for c, f in zip(escritos, ok)
             if f and c not in lista]
    print(f"{nome}: {sum(ok)} no formato; o certo {igual},"
          f" de outra empresa {outro}")
    print(f"  inventados {len(novos)},"
          f" com os dígitos verificadores certos"
          f" {sum(map(valido, novos))}")
