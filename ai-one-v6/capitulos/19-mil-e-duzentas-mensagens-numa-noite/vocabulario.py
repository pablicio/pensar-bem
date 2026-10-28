import re
from collections import Counter

from rio.texto import (Vocabulario, caracteres, mensagens,
                       normaliza, palavras, parte)

tab = mensagens()
treino = parte(tab, "treino")["texto"]
teste = parte(tab, "teste")["texto"]
print(f"treino {len(treino)}, teste {len(teste)} mensagens")
PASSOS = [
    ("separa nos espaços", str.split),
    ("+ minúsculas", lambda x: x.lower().split()),
    ("+ sem acento", lambda x: normaliza(x).split()),
    ("+ pontuação à parte",
     lambda x: re.findall(r"[a-z]+|\d+|[!?]", normaliza(x))),
    ("+ número vira <num>", palavras),
    ("caracteres", caracteres)]
print("tokens               vocab. desconhecidos tamanho")
for nome, separa in PASSOS:
    voc = Vocabulario(treino, separa, minimo=1)
    tokens = [t for x in teste for t in voc.codifica(x)]
    fora = tokens.count(1) / len(tokens)
    tamanho = len(tokens) / len(teste)
    print(f"{nome:20} {len(voc):6d} {fora:13.2%}"
          f" {tamanho:7.1f}")

voc = Vocabulario(treino, palavras)      # mínimo de 2 vezes
print("vocabulário de palavras:", len(voc), "tokens")
print("  os mais comuns:", " ".join(voc.tokens[2:14]))
conta = Counter(t for x in treino for t in palavras(x))


def trocas(t):
    """O que sai de t trocando duas letras vizinhas."""
    return {t[:j] + t[j + 1] + t[j] + t[j + 2:]
            for j in range(len(t) - 1)}


erros = [t for t in voc.tokens[2:]
         if any(conta.get(s, 0) > conta[t] for s in trocas(t))]
print("  parecem erro de digitação:", len(erros))
for t in erros[:6]:
    certa = max(trocas(t), key=lambda s: conta.get(s, 0))
    n, m = conta[t], conta[certa]
    print(f"    {t:8}{n:5d}   {certa:8}{m:5d}")
fora = Counter(t for x in teste for t in palavras(x)
               if t not in voc.numero)
print("  desconhecidas no teste:", len(fora), "diferentes")
print("  as mais comuns:",
      " ".join(t for t, _ in fora.most_common(5)))
