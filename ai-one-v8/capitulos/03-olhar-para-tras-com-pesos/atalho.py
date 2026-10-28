import random

import matplotlib.pyplot as plt
import torch

from influencia import REGIOES, mede
from lupa.alinhamento import ExtratorComAtencao
from lupa.extrator import Extrator, Vocabulario, pares

random.seed(0)
torch.manual_seed(0)
dados = pares()
random.shuffle(dados)
teste, treino = dados[:400], dados[400:]
voc = Vocabulario([e + s for e, s in treino])
longos = [p for p in teste if len(p[0]) >= 150]

sem = Extrator(len(voc))
sem.load_state_dict(torch.load("extrator_rnn.pt"))
com = ExtratorComAtencao(len(voc))
com.load_state_dict(torch.load("extrator_atencao.pt"))
medidas = {"sem atenção": mede(sem, longos, voc),
           "com atenção": mede(com, longos, voc)}
print(f"{'região':17} {'sem atenção':>12} {'com atenção':>12}")
for r in REGIOES:
    a, b = (medidas[m][r] for m in medidas)
    print(f"{r:17} {a:12.1e} {b:12.1e}")

fig, eixo = plt.subplots(figsize=(6.5, 3))
for k, (nome, med) in enumerate(medidas.items()):
    eixo.bar([i + 0.4 * k - 0.2 for i in range(5)],
             [med[r] for r in REGIOES], 0.4, label=nome)
eixo.set_xticks(range(5), REGIOES)
eixo.set_yscale("log")
eixo.set_ylabel("norma do gradiente")
eixo.legend()
fig.tight_layout()
fig.savefig("atalho.png", dpi=300)
