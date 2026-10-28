import random

import matplotlib.pyplot as plt
import torch

from lupa.alinhamento import ExtratorComAtencao
from lupa.extrator import INI, Vocabulario, extrai, lote, pares

random.seed(0)
torch.manual_seed(0)
dados = pares()
random.shuffle(dados)
teste, treino = dados[:400], dados[400:]
voc = Vocabulario([e + s for e, s in treino])
modelo = ExtratorComAtencao(len(voc))
modelo.load_state_dict(torch.load("extrator_atencao.pt"))
modelo.eval()

e, s = max(teste, key=lambda par: len(par[0]))
saida = extrai(modelo, e, voc)
print("certo:", " ".join(s))
print("saída:", " ".join(saida))
x, _, _ = lote([(e, [])], voc)
y = torch.tensor([[INI] + voc.codifica(saida)])
with torch.no_grad():
    modelo(x, y)
pesos = modelo.pesos[0, :len(saida), -len(e):]   # sem o pad
print("\nescreve   olha para (peso)")
for k, token in enumerate(saida):
    w, i = pesos[k].max(dim=0)
    viz = " ".join(e[max(0, i - 2):i + 3])
    print(f"{token:9} {e[i]:12} ({w:.2f})  …{viz}…")

ini = e.index("objeto")
fim = e.index("assinatura", ini) + 1
janela = pesos[:, ini:fim]
fig, eixo = plt.subplots(figsize=(7, 4.5))
eixo.imshow(janela, cmap="Greys", aspect="auto")
eixo.set_xticks(range(fim - ini), e[ini:fim], rotation=90,
                fontsize=6)
eixo.set_yticks(range(len(saida)), saida, fontsize=7)
eixo.set_xlabel("extrato (do objeto à assinatura)")
eixo.set_ylabel("o que o decodificador escreve")
fig.tight_layout()
fig.savefig("mapa.png", dpi=300)
