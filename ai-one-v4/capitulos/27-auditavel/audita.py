import json
from collections import Counter
from pathlib import Path

import numpy as np

from leitora.auditoria import registra
from leitora.carrega import leitora
from leitora.decide import REVISAO, limiar

d = dict(np.load("dados/brutos/cartoes_verao.npz"))
cartoes = np.where(d["partes"] == "validacao")[0]
casa = leitora("modelos/leitora_casa.pt")
lim = limiar(160, 3 * REVISAO)

# a noite: a leitora lê e registra cada resposta
with open("registro.jsonl", "w", encoding="utf-8") as arq:
    lidas = [registra(arq, d["inscricoes"][n], q,
                      d["folhas"][n], casa, lim)
             for n in cartoes for q in range(10)]
print(Counter(r["destino"] for r in lidas))
tamanho = Path("registro.jsonl").stat().st_size
print(f"registro: {tamanho:,} bytes")

# a semana: duas digitadoras por resposta duvidosa
with open("revisao.jsonl", "w", encoding="utf-8") as arq:
    for i, r in enumerate(lidas):
        if r["destino"] == "revisão":
            n, q = cartoes[i // 10], i % 10
            valor = int(d["respostas"][n][q])
            arq.write(json.dumps({
                "inscricao": r["inscricao"],
                "questao": r["questao"],
                "digitadoras": [i % 12 + 1, (i + 5) % 12 + 1],
                "valor": None if valor < 0 else valor}) + "\n")

r = next(r for r in lidas
         if (r["inscricao"], r["questao"]) == (31_877, 9))
print(json.dumps({k: v for k, v in r.items() if k != "caixas"},
                 ensure_ascii=False, indent=1))
c = r["caixas"][0]
print(f"caixa 1: entrada {c['entrada']},"
      f" {len(c['logitos'])} logitos")
