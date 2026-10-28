import math
import re

import torch
import torch.nn.functional as F

from lupa.corpus import prepara
from lupa.escolha import amostra, gulosa
from lupa.gpt import GPT

tok, treino, teste = prepara()
modelo = GPT(len(tok.vocab))
modelo.load_state_dict(torch.load("gpt.pt"))
modelo.eval()
fim = tok.especial["<|fim|>"]
PALAVRA = re.compile(r"[^\W\d_]+")
texto_2026 = tok.decodifica(treino.tolist())
conhecidas = set(PALAVRA.findall(texto_2026))


@torch.no_grad()
def mede(escolhe, B=32, n=300):
    x = torch.full((B, 1), fim)
    surpresa = 0.0
    for _ in range(n):
        logits = modelo(x[:, -modelo.T:])[:, -1]
        prox = escolhe(logits)
        # quanto o próprio modelo, a T = 1, se surpreende
        logp = F.log_softmax(logits, -1).gather(-1, prox)
        surpresa -= logp.sum().item() / math.log(2)
        x = torch.cat([x, prox], dim=1)
    texto = tok.decodifica(x[:, 1:].flatten().tolist())
    atos = texto.split("<|fim|>")[:-1]
    palavras = PALAVRA.findall(texto)
    novas = sum(p not in conhecidas for p in palavras)
    uniformes = sum("uniformes escolares" in a for a in atos)
    return (surpresa / (B * n), 100 * novas / len(palavras),
            100 * uniformes / len(atos),
            100 * len(set(atos)) / len(atos))


atos_2026 = texto_2026.split("<|fim|>")
reais = sum("uniformes escolares" in a for a in atos_2026)
print(f"uniformes escolares em 2026:"
      f" {100 * reais / len(atos_2026):.1f}% dos atos")
print(f"{'escolha':17}{'bits':>6}{'inventadas':>11}"
      f"{'uniformes':>10}{'distintos':>10}")
g = torch.Generator().manual_seed(0)
for nome, escolhe in [
        ("gulosa", gulosa),
        ("T = 0.5", amostra(0.5, gerador=g)),
        ("T = 1", amostra(1.0, gerador=g)),
        ("T = 2", amostra(2.0, gerador=g)),
        ("T = 1, p = 0.9", amostra(1.0, p=0.9, gerador=g)),
        ("T = 2, k = 10", amostra(2.0, k=10, gerador=g)),
        ("T = 2, p = 0.5", amostra(2.0, p=0.5, gerador=g))]:
    medidas = mede(escolhe)
    print(f"{nome:17}{medidas[0]:6.2f}" + "".join(
        f"{m:>9.1f}%" for m in medidas[1:]))
