import time

import torch
from transformers import BertConfig, BertForMaskedLM

from lupa.corpus import prepara
from lupa.gpt import lote, taxa
from lupa.mlm import especiais, mascara

torch.manual_seed(0)
torch.set_num_threads(4)
tok, treino, teste = prepara()
V, T, B, PASSOS = len(tok.vocab), 128, 32, 400
CLS = especiais(V)["[CLS]"]

config = BertConfig(vocab_size=V + 3, hidden_size=128,
                    num_hidden_layers=4, num_attention_heads=4,
                    intermediate_size=512,
                    max_position_embeddings=T,
                    pad_token_id=especiais(V)["[PAD]"])
modelo = BertForMaskedLM(config)
n = sum(p.numel() for p in modelo.parameters())
print(f"{n} parâmetros")


def exemplos(ids, gerador=None):
    x, _ = lote(ids, B, T - 1, gerador)
    x = torch.cat([torch.full((B, 1), CLS), x], dim=1)
    entrada, alvo = mascara(x, V, gerador)
    alvo[:, 0] = -100                   # o [CLS] nunca é alvo
    return entrada, alvo


fixo = torch.Generator().manual_seed(1)
validacao = [exemplos(teste, fixo) for _ in range(10)]
opt = torch.optim.AdamW(modelo.parameters(), lr=1e-3,
                        weight_decay=0.01)
inicio = time.time()
for passo in range(PASSOS):
    for g in opt.param_groups:
        g["lr"] = taxa(passo, 1e-3, 40, PASSOS)
    entrada, alvo = exemplos(treino)
    perda = modelo(input_ids=entrada, labels=alvo).loss
    opt.zero_grad()
    perda.backward()
    opt.step()
    if (passo + 1) % 100 == 0:
        print(f"passo {passo + 1}  perda {perda.item():.3f}")
print(f"treino: {time.time() - inicio:.0f} s")

modelo.eval()
certos = total = 0
with torch.no_grad():
    for entrada, alvo in validacao:
        logits = modelo(input_ids=entrada).logits
        conta = alvo != -100
        acertou = logits.argmax(-1) == alvo
        certos += acertou[conta].sum().item()
        total += conta.sum().item()
print(f"2027: {total} escondidos, acerto {certos / total:.3f}")
