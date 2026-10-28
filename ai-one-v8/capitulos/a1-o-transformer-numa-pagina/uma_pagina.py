import math

import torch

from lupa.gpt import GPT

_ = torch.manual_seed(0)
B, T, V = 2, 8, 2000
modelo = GPT(V, d=128, h=4, L=4).eval()
x = torch.randint(0, V, (B, T))


def mostra(nome, t):
    print(f"{nome:30} {str(tuple(t.shape)):>16}")


with torch.no_grad():
    h = modelo.emb(x) + modelo.pos(torch.arange(T))
    mostra("x (tokens)", x)
    mostra("h = emb[x] + pos", h)
    futuro = torch.ones(T, T, dtype=torch.bool).triu(1)
    for n, b in enumerate(modelo.blocos):
        at = b.atencao
        a = b.norma1(h)
        q, k, v = (at.separa(W(a))
                   for W in (at.W_q, at.W_k, at.W_v))
        notas = q @ k.transpose(-2, -1) / math.sqrt(at.d)
        notas = notas.masked_fill(futuro, -math.inf)
        pesos = notas.softmax(-1)
        o = (pesos @ v).transpose(1, 2).reshape(B, T, -1)
        h = h + at.W_o(o)
        meio = b.adiante.gelu(b.adiante.sobe(b.norma2(h)))
        h = h + b.adiante.desce(meio)
        if n == 0:
            mostra("  q, k, v (por cabeça)", q)
            mostra("  notas, pesos", pesos)
            mostra("  saída da atenção", o)
            mostra("  meio da rede adiante", meio)
            mostra("  h depois do bloco", h)
    logits = modelo.saida(modelo.norma(h))
    mostra("logits", logits)
    dif = (logits - modelo(x)).abs().max().item()
print(f"à mão contra o modelo: {dif:.1e}")
