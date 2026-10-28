import math

import torch
import torch.nn.functional as F

from lupa.corpus import prepara
from lupa.diario import mostra
from lupa.gpt import GPT

tok, treino, teste = prepara()
modelo = GPT(len(tok.vocab))
modelo.load_state_dict(torch.load("gpt.pt"))
modelo.eval()
comeco = ("<|fim|>EXTRATO DO CONTRATO Nº 012/2026\n"
          "Contratante: Município de Alto Bonito."
          " Contratada:")
x = torch.tensor([tok.codifica(comeco)])


@torch.no_grad()
def feixe(x, n, k):
    """Mantém as k sequências de maior log-probabilidade."""
    seqs, notas = x, torch.zeros(1)
    for _ in range(n):
        logits = modelo(seqs[:, -modelo.T:])[:, -1]
        logp = F.log_softmax(logits, -1)
        total = (notas[:, None] + logp).flatten()
        notas, idx = total.topk(k)
        V = logp.shape[1]
        origem, token = idx // V, idx % V      # linha e token
        seqs = torch.cat([seqs[origem], token[:, None]], dim=1)
    # o custo da melhor, em bits: -log2 P
    return seqs[0], -notas[0].item() / math.log(2)


for k in [1, 4, 16]:
    seq, bits = feixe(x, 40, k)
    print(f"--- feixe de {k}: {bits:.1f} bits")
    mostra(tok.decodifica(seq[x.shape[1]:].tolist()))
