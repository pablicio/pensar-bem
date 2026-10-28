import math
import time

import matplotlib.pyplot as plt
import torch

from lupa.corpus import prepara
from lupa.gpt import GPT, lote, taxa

torch.manual_seed(0)
torch.set_num_threads(4)
tok, treino, teste = prepara()
V, T, B, PASSOS = len(tok.vocab), 128, 32, 600

modelo = GPT(V, T)
n = sum(p.numel() for p in modelo.parameters())
print(f"{n} parâmetros")
x, y = lote(treino, B, T)
print(f"perda inicial {modelo(x, y).item():.2f}, ln V ="
      f" {math.log(V):.2f}")

# decaimento só nas matrizes; não nos vieses nem nas normas
matrizes = [p for p in modelo.parameters() if p.dim() >= 2]
vetores = [p for p in modelo.parameters() if p.dim() < 2]
grupos = [{"params": matrizes, "weight_decay": 0.1},
          {"params": vetores, "weight_decay": 0.0}]
opt = torch.optim.AdamW(grupos, lr=3e-3, betas=(0.9, 0.95))
fixo = torch.Generator().manual_seed(1)
validacao = [lote(teste, B, T, fixo) for _ in range(10)]


@torch.no_grad()
def avalia():
    modelo.eval()
    p = sum(modelo(x, y).item() for x, y in validacao) / 10
    modelo.train()
    return p


curva_treino, curva_val = [], []
inicio = time.time()
for passo in range(PASSOS):
    for g in opt.param_groups:
        g["lr"] = taxa(passo, 3e-3, 50, PASSOS)
    x, y = lote(treino, B, T)
    perda = modelo(x, y)
    opt.zero_grad()
    perda.backward()
    torch.nn.utils.clip_grad_norm_(modelo.parameters(), 1.0)
    opt.step()
    curva_treino.append(perda.item())
    if (passo + 1) % 100 == 0:
        curva_val.append((passo + 1, avalia()))
        print(f"passo {passo + 1:4}  treino {perda.item():.3f}"
              f"  validação {curva_val[-1][1]:.3f}")
print(f"treino: {time.time() - inicio:.0f} s")
torch.save(modelo.state_dict(), "gpt.pt")

bits = avalia() / math.log(2)
print(f"2027: {bits:.3f} bits por token,"
      f" perplexidade {2 ** bits:.2f}")

fig, eixo = plt.subplots(figsize=(6, 3))
eixo.plot(curva_treino, label="treino (um lote)", alpha=0.6)
eixo.plot(*zip(*curva_val), "o-", label="validação (2027)")
eixo.axhline(2.744 * math.log(2), ls="--", color="gray",
             label="bigramas")
eixo.set_xlabel("passo")
eixo.set_ylabel("perda (nats por token)")
eixo.set_ylim(0, 4)
eixo.legend()
fig.tight_layout()
fig.savefig("gpt_pequeno.png", dpi=300)
