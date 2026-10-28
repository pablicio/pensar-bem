import sys

import matplotlib.pyplot as plt
import torch

from dados.inverno import GABARITO, VALENTINA
from dados.inverno import cartao_do_inverno
from leitora.auditoria import registra, rele
from leitora.carrega import leitora
from leitora.decide import REVISAO, TEMPERATURA, limiar
from leitora.noite import le_cartao
from leitora.recorte import caixa

casa = leitora("modelos/leitora_casa.pt")
lim = limiar(160, 3 * REVISAO)

# sexta: a nota da Valentina
inscricao, folha, _, _ = cartao_do_inverno(VALENTINA)
lidas = le_cartao(casa, folha)
nota = sum(lido == gab
           for (_, lido, _), gab in zip(lidas, GABARITO))
revistas = sum(p < lim for _, _, p in lidas)
print(f"inscrição {inscricao}: {nota} de 10,"
      f" {revistas} revistas pelas digitadoras\n")

# sábado: a contestação
CONTESTADO, QUESTAO = int(sys.argv[1]), int(sys.argv[2])
i = CONTESTADO - 60_000
inscricao, folha, respostas, _ = cartao_do_inverno(i)
with open("contestacao.jsonl", "w", encoding="utf-8") as arq:
    r = registra(arq, inscricao, QUESTAO - 1, folha, casa, lim)
print(f"inscrição {inscricao}, questão {QUESTAO}:")
print(f"  leitora {r['modelo']}, cartão {r['cartao']}")
for k, c in enumerate(r["caixas"]):
    if c is None:
        print(f"  caixa {k + 1}: em branco")
        continue
    p = (torch.tensor(c["logitos"]) / TEMPERATURA).softmax(0)
    (p1, p2), (d1, d2) = (v.tolist() for v in p.topk(2))
    print(f"  caixa {k + 1}: leu {d1} com {p1:.4f};"
          f" depois, {d2} com {p2:.4f}")
print(f"  texto [{r['texto']}],"
      f" confiança {r['confianca']:.4f},"
      f" limiar {r['limiar']:.3f}: {r['destino']}")
print("  releitura:", rele(r, folha, casa))
print(f"  gabarito {GABARITO[QUESTAO - 1]}; no papel,"
      f" {respostas[QUESTAO - 1]}")

fig, eixos = plt.subplots(1, 3, figsize=(4.5, 1.8))
for k, ax in enumerate(eixos):
    ax.imshow(caixa(folha, QUESTAO - 1, k), cmap="gray_r")
    ax.axis("off")
fig.tight_layout()
fig.savefig("contestada.png", dpi=400)
