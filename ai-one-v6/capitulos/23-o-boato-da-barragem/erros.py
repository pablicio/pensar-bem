import numpy as np

from rio.texto import CLASSES, mensagens, parte
from rio.triagem import carrega, triagem

voc, leitor, bayes = carrega()
teste = parte(mensagens(), "teste")
p = triagem(teste["texto"], voc, leitor, bayes)
prevista = np.array(CLASSES)[p.argmax(1)]
julia = teste["classe"].to_numpy()
verdade = teste["verdade"].to_numpy()
texto = teste["texto"].str.slice(0, 38).to_numpy()
discorda = np.flatnonzero(prevista != julia)
confianca = p.max(1)
ordem = discorda[np.argsort(-confianca[discorda])]
ela = ordem[prevista[ordem] == verdade[ordem]]
dele = ordem[prevista[ordem] != verdade[ordem]]
print(f"o modelo discorda da Júlia em {len(discorda)}"
      f" de {len(teste)} mensagens")
print(f"  a Júlia errou em {len(ela)},"
      f" o modelo em {len(dele)}")
print("entre as 20 mais confiantes, o modelo errou em",
      np.isin(ordem[:20], dele).sum())
print("as 8 primeiras (Júlia -> modelo):")
for i in ordem[:8]:
    c, de, para = confianca[i], julia[i], prevista[i]
    print(f"  {c:.2f} {de:5} -> {para:5} {texto[i]}")
print("os erros do modelo (verdade -> modelo, P da verdade):")
for i in dele:
    k = CLASSES.index(verdade[i])
    print(f"  {p[i, k]:.2f} {verdade[i]:5} -> {prevista[i]:5}"
          f" {texto[i]}")
