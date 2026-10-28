import time

import matplotlib.pyplot as plt
import torch

from lupa.bert import BERT
from lupa.corpus import prepara
from lupa.gpt import lote, taxa
from lupa.mlm import mascara

torch.set_num_threads(4)
tok, treino, teste = prepara()
V, T, B = len(tok.vocab), 128, 32
fixo = torch.Generator().manual_seed(1)
validacao = [mascara(lote(teste, B, T, fixo)[0], V, fixo)
             for _ in range(10)]

curvas = {}
for posicao, passos in [("aprendida", 300), ("rope", 600)]:
    torch.manual_seed(0)
    modelo = BERT(V, T, posicao=posicao)
    opt = torch.optim.AdamW(modelo.parameters(), lr=3e-3,
                            weight_decay=0.01)
    curvas[posicao] = []
    inicio = time.time()
    for passo in range(passos):
        for g in opt.param_groups:
            g["lr"] = taxa(passo, 3e-3, 30, passos)
        x, _ = lote(treino, B, T)
        perda = modelo.perda_mlm(*mascara(x, V))
        opt.zero_grad()
        perda.backward()
        opt.step()
        curvas[posicao].append(perda.item())
        if (passo + 1) % 100 == 0:
            print(f"{posicao:9} passo {passo + 1}"
                  f"  perda {perda.item():.3f}")
    print(f"{posicao}: {time.time() - inicio:.0f} s")

torch.save(modelo.state_dict(), "bert.pt")      # o de RoPE
n = sum(p.numel() for p in modelo.parameters())
print(f"\nBERT com RoPE: {n} parâmetros")

modelo.eval()
digitos = {i for i in range(V)
           if tok.vocab[i].strip().isdigit()}
conta = {"dígitos": [0, 0], "o resto": [0, 0]}
with torch.no_grad():
    for entrada, alvo in validacao:
        palpite = modelo.saida(modelo(entrada)).argmax(-1)
        for a, p in zip(alvo.flatten().tolist(),
                        palpite.flatten().tolist()):
            if a == -100:
                continue
            tipo = "dígitos" if a in digitos else "o resto"
            c = conta[tipo]
            c[0] += a == p
            c[1] += 1
for nome, (certos, total) in conta.items():
    print(f"2027, {nome}: {total} escondidos,"
          f" acerto {certos / total:.3f}")

fig, eixo = plt.subplots(figsize=(6, 3))
for posicao, perdas in curvas.items():
    eixo.plot(perdas, label=f"posição {posicao}", alpha=0.8)
eixo.set_xlabel("passo")
eixo.set_ylabel("perda nos tokens escondidos")
eixo.legend()
fig.tight_layout()
fig.savefig("treina_bert.png", dpi=300)
