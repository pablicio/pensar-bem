import json

import numpy as np

from leitora.auditoria import rele
from leitora.carrega import leitora

GABARITO = [42, 7, 315, 128, 9, 640, 77, 501, 18, 999]
INSCRICAO = 31_877

with open("registro.jsonl", encoding="utf-8") as arq:
    lidas = [json.loads(linha) for linha in arq]
with open("revisao.jsonl", encoding="utf-8") as arq:
    revistas = {(r["inscricao"], r["questao"]): r
                for r in map(json.loads, arq)}

print(f"{'questão':7} {'lido':>5}  {'quem leu':18}"
      f" {'final':>5} {'gabarito':>9}")
nota = 0
for r in lidas:
    if r["inscricao"] != INSCRICAO:
        continue
    q, lido = r["questao"], r["lido"]
    quem, final = "a leitora", lido
    if (INSCRICAO, q) in revistas:
        rev = revistas[(INSCRICAO, q)]
        a, b = rev["digitadoras"]
        quem = f"digitadoras {a} e {b}"
        final = rev["valor"]
    certa = final == GABARITO[q - 1]
    nota += certa
    print(f"{q:7} {lido!s:>5}  {quem:18} {final!s:>5}"
          f" {GABARITO[q - 1]:9}{'  certa' if certa else ''}")
print(f"nota: {nota} de 10\n")

# meses depois: o mesmo cartão, a leitora guardada
d = dict(np.load("dados/brutos/cartoes_verao.npz"))
folha = d["folhas"][d["inscricoes"] == INSCRICAO][0]
r = next(r for r in lidas
         if (r["inscricao"], r["questao"]) == (INSCRICAO, 9))
print("leitora da casa:", rele(r, folha, leitora(
    "modelos/leitora_casa.pt")))
print("leitora do MNIST:", rele(r, folha, leitora(
    "modelos/leitora_mnist.pt")))
outra = folha.copy()
outra[300, 100] += 1                # um pixel, uma unidade
print("cartão escaneado de novo:", rele(r, outra, leitora(
    "modelos/leitora_casa.pt")))
