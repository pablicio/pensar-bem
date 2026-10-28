import numpy as np

from rio.provinha import PROVINHA
from rio.texto import mensagens, parte
from rio.triagem import carrega, triagem

SILENCIO = 50    # um pedido real jogado na pilha dos boatos
BOATO = 1        # um boato que a Júlia lê e responde à mão
voc, leitor, bayes = carrega()
tab = mensagens()
valid, teste = parte(tab, "validacao"), parte(tab, "teste")
p_v = triagem(valid["texto"], voc, leitor, bayes)[:, 3]
pedido = valid["classe"].isin(["risco", "ajuda"]).to_numpy()
boato = (valid["classe"] == "boato").to_numpy()
print("validação, pelos rótulos da Júlia")
print("limiar  na pilha  pedidos  boatos fora  custo")
custos = {}
for limiar in (0.5, 0.8, 0.9, 0.95, 0.99, 0.999):
    pilha = p_v > limiar
    calados = np.sum(pilha & pedido)
    fora = np.sum(~pilha & boato)
    custos[limiar] = calados * SILENCIO + fora * BOATO
    print(f"{limiar:6} {pilha.sum():9d} {calados:8d}"
          f" {fora:12d} {custos[limiar]:6d}")
limiar = min(custos, key=custos.get)
calados = valid[(p_v > limiar) & pedido]
print(f"limiar {limiar}; os {len(calados)} pedidos na pilha")
print("  eram, de verdade:", " ".join(calados["verdade"]))
p_t = triagem(teste["texto"], voc, leitor, bayes)
pilha = p_t[:, 3] > limiar
real = teste["verdade"].isin(["risco", "ajuda"]).to_numpy()
print(f"teste: {pilha.sum()} na pilha, pedidos calados:"
      f" {np.sum(pilha & real)}")
disfarce = (teste["texto"].str.contains("pedindo socorro")
            & (teste["verdade"] == "boato")).to_numpy()
print(f"  boatos disfarçados de pedido: {disfarce.sum()},"
      f" na pilha {np.sum(pilha & disfarce)}")
maior = p_t[disfarce, 0].max()
print(f"  maior P(risco) entre eles: {maior:.2f}")
p_p = triagem([t for t, _ in PROVINHA], voc, leitor, bayes)
classe = np.array([c for _, c in PROVINHA])
pedidos = np.isin(classe, ["risco", "ajuda"])
print(f"provinha: maior P(boato) de um pedido"
      f" {p_p[pedidos, 3].max():.2f}")
print(f"  boatos na pilha:"
      f" {np.sum(p_p[classe == 'boato', 3] > limiar)} de 6")
