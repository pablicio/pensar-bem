import contextlib
import io
import random

import torch

from lupa.extrator import (PAD, Vocabulario, acertos, lote,
                           pares, treina)
from lupa.qkv_rnn import ExtratorQKV

random.seed(0)
torch.manual_seed(0)
dados = pares()
random.shuffle(dados)
teste, treino = dados[:400], dados[400:]
voc = Vocabulario([e + s for e, s in treino])
x, _, _ = lote(teste[:64], voc)       # um lote fixo para medir


@torch.no_grad()
def notas_iniciais(m):
    """O desvio das notas e o maior peso no primeiro passo do
    decodificador, num lote fixo do teste."""
    estados, h = m.cod(m.emb(x))
    notas = torch.einsum("bd,btd->bt", m.W_q(h[-1]),
                         m.W_k(estados)) / m.divisor
    notas = notas.masked_fill(x == PAD, float("-inf"))
    maior = notas.softmax(-1).max(-1).values.mean().item()
    return notas[x != PAD].std().item(), maior


modelos = {}
for escala in [True, False]:
    torch.manual_seed(0)
    modelos[escala] = ExtratorQKV(len(voc), escala=escala)
print("época   com √d: desvio  maior   sem √d: desvio  maior")
for ep in range(1, 11):
    medidas = []
    for escala, m in modelos.items():
        random.seed(ep)
        with contextlib.redirect_stdout(io.StringIO()):
            treina(m, treino, voc, epocas=1)
        medidas += notas_iniciais(m)
    a, b, c, d = medidas
    print(f"{ep:5} {a:15.2f} {b:6.2f} {c:15.2f} {d:6.2f}")

linhas = acertos(modelos[False], teste, voc)
FAIXAS = [(0, 120), (120, 160), (160, 200), (200, 400)]
print("\nsem √d: tokens  prazo  valor")
for lo, hi in FAIXAS:
    sel = [x[1:3] for x in linhas if lo <= x[0] < hi]
    p, v = [sum(c) / len(sel) for c in zip(*sel)]
    print(f"        {lo:3}–{hi:<3} {p:5.0%} {v:6.0%}")
