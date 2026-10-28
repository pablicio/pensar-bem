import copy
import time

import torch
import torch.nn.functional as F

from lupa.corpus import prepara
from lupa.diario import atos, gabarito
from lupa.extrator import limpa
from lupa.gpt import GPT
from lupa.instrucao import (logp_resposta, pergunta, resposta,
                            respostas, responde)

torch.set_num_threads(4)
tok, _, _ = prepara()
V = len(tok.vocab)
PAD = tok.especial["<|fim|>"]
verdade = gabarito()
instruido = GPT(V)
instruido.load_state_dict(torch.load("instruido.pt"))
instruido.eval()
NAO = "Não consta."


def casos(de_2027, n):
    """Atos com contratada e atos sem, com a resposta certa."""
    com, sem = [], []
    for a in atos():
        if (a["data"] >= "2027") != de_2027:
            continue
        g = verdade[a["id"]]
        p = pergunta(tok, a["texto"], "CONTRATADA")
        if g["entidades"]:
            certa = respostas(a["texto"], g["entidades"])
            com.append((p, certa["CONTRATADA"]))
        elif "Contratada" not in limpa(a["texto"]):
            sem.append((p, NAO))
    return com[:n], sem[:n]


def mede(modelo, nome):
    modelo.eval()
    certos = sum(responde(modelo, tok, p) == r
                 for p, r in com_t)
    nao = sum(responde(modelo, tok, p) == NAO
              for p, _ in sem_t)
    print(f"{nome}:")
    print(f"  contratada certa: {certos}/{len(com_t)}")
    print(f"  \"{NAO}\" nos atos sem: {nao}/{len(sem_t)}")
    print("  um ato sem contratada:",
          responde(modelo, tok, sem_t[0][0]))


com_t, sem_t = casos(True, 150)
mede(instruido, "instruído")

# (pergunta, preferida, rejeitada), com atos de 2026; nos atos
# sem contratada, a rejeitada é o que o instruído responde
com, sem = casos(False, 300)
pares = [(p, resposta(tok, NAO),
          resposta(tok, responde(instruido, tok, p)))
         for p, _ in sem]
pares += [(p, resposta(tok, r), resposta(tok, NAO))
          for p, r in com]


def dpo(lam, beta=0.1, epocas=2):
    """DPO a partir do instruído; lam pesa -log p(boa)."""
    torch.manual_seed(0)
    politica = copy.deepcopy(instruido)
    opt = torch.optim.AdamW(politica.parameters(), lr=1e-4)
    for epoca in range(epocas):
        politica.train()
        for k in torch.randperm(len(pares)).split(16):
            lote = [pares[i] for i in k]
            boa = [(p, a) for p, a, _ in lote]
            ruim = [(p, b) for p, _, b in lote]
            with torch.no_grad():
                ref_boa = logp_resposta(instruido, boa, PAD)
                ref_ruim = logp_resposta(instruido, ruim, PAD)
            lp_boa = logp_resposta(politica, boa, PAD)
            lp_ruim = logp_resposta(politica, ruim, PAD)
            margem = (lp_boa - ref_boa) - (lp_ruim - ref_ruim)
            tamanho = torch.tensor([len(a) for _, a in boa])
            perda = (-F.logsigmoid(beta * margem)
                     - lam * lp_boa / tamanho).mean()
            opt.zero_grad()
            perda.backward()
            opt.step()
        print(f"  época {epoca + 1}: log p da boa"
              f" {lp_boa.mean().item():6.1f},"
              f" da ruim {lp_ruim.mean().item():6.1f}")
    return politica


with torch.no_grad():
    antes = logp_resposta(instruido, [(p, a) for p, a, _
                                      in pares[:16]], PAD)
print(f"{len(pares)} pares; log p(\"{NAO}\") no instruído:"
      f" {antes.mean().item():.1f}")
for lam in [0.0, 1.0]:
    inicio = time.time()
    print(f"DPO, lambda = {lam:g}")
    politica = dpo(lam)
    print(f"  {time.time() - inicio:.0f} s")
    mede(politica, f"DPO, lambda = {lam:g}")
torch.save(politica.state_dict(), "preferencias.pt")
