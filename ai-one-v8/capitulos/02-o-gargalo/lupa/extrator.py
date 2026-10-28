"""O extrator recorrente: lê um extrato e escreve o prazo e o
valor, como o Renan montou em 2025 (o encoder-decoder do
volume 6)."""
import random
import re
import unicodedata

import torch
from torch import nn

from .diario import atos

TOKEN = re.compile(r"\d|\w+|[^\w\s]")
PRAZO = re.compile(r"Prazo: (\d+ \([\w ]+\) \w+)")
VALOR = re.compile(r"Valor: (R\$ [\d.,]+\d)")
PAD, INI, FIM, DESC = 0, 1, 2, 3


def limpa(texto):
    """Desfaz o que o PDF fez (o capítulo 15 explica)."""
    texto = unicodedata.normalize("NFC", texto)
    return texto.replace("-\n", "")


def tokens(texto):
    return TOKEN.findall(limpa(texto).lower())


def pares():
    """(extrato, 'prazo ; valor'), com o alvo tirado por
    expressões regulares, como o Renan fez os rótulos."""
    lista = []
    for a in atos():
        if a["tipo"] != "extrato":
            continue
        texto = limpa(a["texto"])
        prazo, valor = PRAZO.search(texto), VALOR.search(texto)
        alvo = f"{prazo.group(1)} ; {valor.group(1)}"
        lista.append((tokens(texto), tokens(alvo)))
    return lista


class Vocabulario:
    def __init__(self, sequencias, minimo=2):
        conta = {}
        for seq in sequencias:
            for t in seq:
                conta[t] = conta.get(t, 0) + 1
        frequentes = [t for t, n in conta.items()
                      if n >= minimo]
        self.itos = ["<pad>", "<ini>", "<fim>", "<?>"]
        self.itos += sorted(frequentes)
        self.stoi = {t: i for i, t in enumerate(self.itos)}

    def codifica(self, seq):
        return [self.stoi.get(t, DESC) for t in seq]

    def __len__(self):
        return len(self.itos)


def lote(pares, voc):
    """Entradas com o preenchimento à esquerda; alvos com
    <ini> na entrada do decodificador e <fim> na saída."""
    E = max(len(e) for e, _ in pares)
    S = max(len(s) for _, s in pares) + 1
    x = torch.full((len(pares), E), PAD)
    y_in = torch.full((len(pares), S), PAD)
    y_out = torch.full((len(pares), S), PAD)
    for k, (e, s) in enumerate(pares):
        ce, cs = voc.codifica(e), voc.codifica(s)
        x[k, E - len(ce):] = torch.tensor(ce)
        y_in[k, :len(cs) + 1] = torch.tensor([INI] + cs)
        y_out[k, :len(cs) + 1] = torch.tensor(cs + [FIM])
    return x, y_in, y_out


class Extrator(nn.Module):
    """Codificador e decodificador recorrentes: o extrato
    completo vira um vetor, e o vetor vira a resposta."""

    def __init__(self, n_voc, emb=64, oculto=128):
        super().__init__()
        self.emb = nn.Embedding(n_voc, emb, padding_idx=PAD)
        self.cod = nn.GRU(emb, oculto, batch_first=True)
        self.dec = nn.GRU(emb, oculto, batch_first=True)
        self.saida = nn.Linear(oculto, n_voc)

    def forward(self, x, y_in):
        _, h = self.cod(self.emb(x))     # o vetor do extrato
        o, _ = self.dec(self.emb(y_in), h)
        return self.saida(o)


def treina(modelo, treino, voc, epocas, lr=3e-3, lote_n=32):
    opt = torch.optim.Adam(modelo.parameters(), lr)
    perda_fn = nn.CrossEntropyLoss(ignore_index=PAD)
    for ep in range(1, epocas + 1):
        random.shuffle(treino)
        total = 0.0
        for k in range(0, len(treino), lote_n):
            x, y_in, y_out = lote(treino[k:k + lote_n], voc)
            logits = modelo(x, y_in)
            perda = perda_fn(logits.flatten(0, 1),
                             y_out.flatten())
            opt.zero_grad()
            perda.backward()
            opt.step()
            total += perda.item()
        n = (len(treino) + lote_n - 1) // lote_n
        print(f"época {ep:2}  perda {total / n:.3f}")


@torch.no_grad()
def extrai(modelo, entrada, voc, maximo=24):
    """Decodificação gulosa: a palavra mais provável a cada
    passo, até <fim>."""
    x, _, _ = lote([(entrada, [])], voc)
    y = torch.tensor([[INI]])
    for _ in range(maximo):
        proxima = modelo(x, y)[0, -1].argmax().item()
        if proxima == FIM:
            break
        y = torch.cat([y, torch.tensor([[proxima]])], dim=1)
    return [voc.itos[i] for i in y[0, 1:].tolist()]


def acertos(modelo, teste, voc):
    """Para cada extrato do teste: o tamanho, se acertou o
    prazo, o valor, a quantidade de dígitos do valor e a fração
    de dígitos certos."""
    modelo.eval()
    linhas = []
    for e, s in teste:
        saida = extrai(modelo, e, voc)
        k = s.index(";")
        certo = [t for t in s[k + 1:] if t.isdigit()]
        feito = [t for t in saida[k + 1:] if t.isdigit()]
        digitos = sum(a == b for a, b in zip(certo, feito))
        linhas.append((len(e), saida[:k] == s[:k],
                       saida[k + 1:] == s[k + 1:],
                       len(feito) == len(certo),
                       digitos / len(certo)))
    return linhas


def influencia(modelo, par, voc):
    """Quanto cada token da entrada pesa no valor escrito: a
    norma do gradiente de log P(valor) em relação ao embedding
    de cada token, do último (índice 0) para o primeiro."""
    vistos = []
    gancho = modelo.emb.register_forward_hook(
        lambda modulo, ent, sai: vistos.append(sai))
    x, y_in, y_out = lote([par], voc)
    logits = modelo(x, y_in)
    gancho.remove()
    k = par[1].index(";")
    pos = torch.arange(k + 1, len(par[1]))  # tokens do valor
    logp = logits[0].log_softmax(-1)[pos, y_out[0, pos]].sum()
    (g,) = torch.autograd.grad(logp, vistos[0])
    normas = g[0].norm(dim=-1)[-len(par[0]):]
    return normas.flip(0)
