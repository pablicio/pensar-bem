import re

import numpy as np
import torch

from lupa.ajuste import Classificador, tensores
from lupa.bert import BERT
from lupa.corpus import prepara
from lupa.diario import gabarito, le
from lupa.extrator import limpa

tok, _, _ = prepara()
modelo = Classificador(BERT(len(tok.vocab)))
modelo.load_state_dict(torch.load("relevancia.pt"))
modelo.eval()
verdade = gabarito()
atos = [a for a in le("producao.jsonl")
        if a["data"] < "2027-05"]          # fevereiro a abril
ids, vazio = tensores([a["texto"] for a in atos], tok)
with torch.no_grad():
    p = torch.cat([modelo(ids[i:i + 128], vazio[i:i + 128])
                   .softmax(-1)[:, 1]
                   for i in range(0, len(ids), 128)]).numpy()
alerta = p > 0.5
real = np.array([verdade[a["id"]]["relevante"] for a in atos])


def wilson(x, n, z=1.96):
    """O intervalo de Wilson para uma proporção x / n."""
    q = x / n
    centro = (q + z * z / (2 * n)) / (1 + z * z / n)
    meia = (z / (1 + z * z / n)
            * np.sqrt(q * (1 - q) / n + z * z / (4 * n * n)))
    return centro - meia, centro + meia


def wald(x, n, z=1.96):
    q = x / n
    meia = z * np.sqrt(q * (1 - q) / n)
    return q - meia, q + meia


x, n = int((alerta & real).sum()), int(alerta.sum())
print(f"precisão {x}/{n} = {x / n:.3f}")
print("  Wald   [{:.3f}, {:.3f}]".format(*wald(x, n)))
print("  Wilson [{:.3f}, {:.3f}]".format(*wilson(x, n)))

# kappa: o acordo com o gabarito, descontado o do acaso
a_, r_ = alerta.mean(), real.mean()
po = (alerta == real).mean()
pe = a_ * r_ + (1 - a_) * (1 - r_)
print(f"acordo {po:.4f}, acordo por acaso {pe:.4f},"
      f" kappa {(po - pe) / (1 - pe):.3f}")

# quantas obras o sistema perdeu? só lendo os descartados
nao = ~alerta
suspeitos = nao & (p >= 0.001)      # onde o modelo hesita
calmos = nao & (p < 0.001)
print(f"descartados {nao.sum()}: {suspeitos.sum()} suspeitos,"
      f" {calmos.sum()} calmos")
rng = np.random.default_rng(0)
simples, estratos = [], []
for _ in range(2000):
    # 135 leituras sorteadas entre todos os descartados...
    s = rng.choice(np.where(nao)[0], 135, replace=False)
    simples.append(real[s].mean() * nao.sum())
    # ...ou os 35 suspeitos e 100 sorteados entre os calmos
    c = rng.choice(np.where(calmos)[0], 100, replace=False)
    estratos.append(real[suspeitos].sum()
                    + real[c].mean() * calmos.sum())
for nome, e in [("sorteio simples", simples),
                ("por estratos", estratos)]:
    print(f"  {nome:16} perdidas: média {np.mean(e):5.1f},"
          f" desvio {np.std(e):5.1f}")
print(f"  de verdade: {(nao & real).sum()}")
alto = wilson(0, 100)[1]
print(f"0 em 100 calmos: até {alto:.3f} x {calmos.sum()}"
      f" = {alto * calmos.sum():.0f} perdidas, com 95%")

# análise de erro: o que as perdidas têm em comum
perdidas = np.where(nao & real)[0]
raras = sum(verdade[atos[i]["id"]]["raro"] for i in perdidas)
print(f"\nas {len(perdidas)} perdidas: {raras} com palavras"
      " raras")
OBJETO = re.compile(r"Objeto(?: do contrato)?:\s*(\S+ \S+)",
                    re.IGNORECASE)
vezes = {}
for i in perdidas:
    m = OBJETO.search(limpa(atos[i]["texto"]))
    inicio = m.group(1).lower()
    vezes[inicio] = vezes.get(inicio, 0) + 1
for inicio, n in sorted(vezes.items(), key=lambda x: -x[1]):
    print(f"  {n}  {inicio}")
