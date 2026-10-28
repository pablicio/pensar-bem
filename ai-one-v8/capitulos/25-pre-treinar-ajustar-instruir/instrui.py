import time

import torch

from lupa.corpus import prepara
from lupa.diario import atos, gabarito, le, mostra
from lupa.gpt import GPT
from lupa.instrucao import (PERGUNTAS, lote, pergunta,
                            resposta, respostas, responde)

torch.manual_seed(0)
torch.set_num_threads(4)
tok, _, _ = prepara()
V = len(tok.vocab)
corpus = {a["id"]: a for a in atos()}
PAD = tok.especial["<|fim|>"]


def pares(itens):
    saida = []
    for ident, entidades in itens:
        texto = corpus[ident]["texto"]
        for chave, r in respostas(texto, entidades).items():
            p = pergunta(tok, texto, chave)
            q = resposta(tok, r)
            if len(p) + len(q) <= 128:     # cabe no contexto
                saida.append((p, q, chave, r))
    return saida


treino = pares((r["id"], r["entidades"])
               for r in le("rotulos.jsonl") if r["entidades"]
               and corpus[r["id"]]["data"] < "2027")
teste = pares((i, g["entidades"])
              for i, g in gabarito().items()
              if g["entidades"] and i in corpus
              and corpus[i]["data"] >= "2027")
print(f"{len(treino)} perguntas de treino,"
      f" {len(teste)} de teste")
mostra(tok.decodifica(treino[1][0] + treino[1][1])[-120:])


def avalia(modelo, nome):
    modelo.eval()
    certos = {c: [0, 0] for c in PERGUNTAS}
    for p, _, chave, r in teste:
        certos[chave][0] += responde(modelo, tok, p) == r
        certos[chave][1] += 1
    print(nome + ": " + ", ".join(
        f"{c.lower()} {a / n:.0%}"
        for c, (a, n) in certos.items()))


modelo = GPT(V)
modelo.load_state_dict(torch.load("gpt.pt"))
avalia(modelo, "GPT sem ajuste")

opt = torch.optim.AdamW(modelo.parameters(), lr=1e-3)
modelo.train()
inicio = time.time()
for epoca in range(10):
    ordem = torch.randperm(len(treino))
    for k in range(0, len(treino), 16):
        escolhidos = [treino[i][:2] for i in ordem[k:k + 16]]
        x, y = lote(escolhidos, PAD)
        perda = modelo(x, y)
        opt.zero_grad()
        perda.backward()
        opt.step()
    print(f"época {epoca + 1}  perda {perda.item():.3f}")
print(f"ajuste: {time.time() - inicio:.0f} s")
torch.save(modelo.state_dict(), "instruido.pt")
avalia(modelo, "GPT instruído")
