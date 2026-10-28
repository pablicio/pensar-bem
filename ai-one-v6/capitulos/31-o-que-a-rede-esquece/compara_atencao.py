import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from rio.atencao import ExtratorComAtencao
from rio.extrator import (CAMPOS, Extrator, registro,
                          vocabularios)
from rio.leitor import preenche
from rio.texto import mensagens, parte

tab = mensagens()
pedidos = tab[tab["verdade"].isin(["risco", "ajuda"])]
treino = parte(pedidos, "treino")
teste = parte(pedidos, "teste")
registros = [registro(l) for _, l in treino.iterrows()]
entrada, saida = vocabularios(treino["texto"], registros)
certo = [registro(l) for _, l in teste.iterrows()]
x, n = preenche(entrada, teste["texto"], maximo=240)
gerados = {}
for nome, classe, arquivo in [
        ("contexto", Extrator, "extrator.pt"),
        ("atenção", ExtratorComAtencao, "atencao.pt")]:
    modelo = classe(len(entrada), len(saida))
    modelo.load_state_dict(torch.load(arquivo))
    gerados[nome] = modelo.extrai(x, n, saida)


def campo(r, k):
    partes = r.split("|")
    return partes[k] if len(partes) == 4 else None


print("campo     contexto  atenção")
for k, c in enumerate(CAMPOS):
    taxas = [np.mean([campo(g, k) == campo(r, k)
                      for g, r in zip(gerados[m], certo)])
             for m in gerados]
    print(f"{c:8} {taxas[0]:9.1%} {taxas[1]:8.1%}")
FAIXAS = [(0, 60), (60, 100), (100, 140), (140, 240)]
print("caracteres  registro exato: contexto  atenção")
for a, b in FAIXAS:
    s = (n.numpy() >= a) & (n.numpy() < b)
    taxas = [np.mean([g == r for g, r, ok in
                      zip(gerados[m], certo, s) if ok])
             for m in gerados]
    print(f"{a:3d} a {b:3d} {taxas[0]:22.1%} {taxas[1]:8.1%}")
# o que o decoder olhou ao escrever o registro da Dona Ivone
ivone = teste["texto"].str.endswith("ivone").to_numpy()
texto = teste["texto"][ivone].iloc[0]
xi, ni = x[ivone.copy()], n[ivone.copy()]
escrito = modelo.extrai(xi, ni, saida)[0]
print("Dona Ivone:", escrito)
y = preenche(saida, ["^" + escrito + "$"], 62)[0]
with torch.no_grad():
    memoria, estado = modelo.le(xi, ni)
    entrada_d = modelo.emb_s(y[:, :len(escrito) + 1])
    d, _ = modelo.decoder(entrada_d, estado)
    _, pesos = modelo.olha(d, memoria, xi != 0)
fig, ax = plt.subplots(figsize=(8, 3.2))
ax.imshow(pesos[0, :, :int(ni)].numpy(), aspect="auto",
          cmap="Greys")
letras = list(texto.lower())
ax.set_xticks(range(len(letras)), letras, fontsize=5)
ax.set_yticks(range(len(escrito) + 1), list(escrito) + ["$"],
              fontsize=6)
fig.tight_layout()
fig.savefig("atencao.png", dpi=300)
