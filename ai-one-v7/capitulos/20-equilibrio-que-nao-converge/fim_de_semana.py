import matplotlib.pyplot as plt
import torch

from lauber.acervo import carrega, grade, partes
from lauber.dcgan import CODIGO, Gerador, Perito, inicia
from lauber.wgan import fatiada, treina

imgs, _ = carrega()
treino, _, teste = partes(len(imgs))
referencia = imgs[teste][:500]
print(f"régua entre duas partes do acervo:"
      f" {fatiada(imgs[treino][:500], referencia):.3f}")

torch.manual_seed(0)
gerador, perito = Gerador(), Perito()
gerador.apply(inicia)
perito.apply(inicia)
fotos, historico = treina(gerador, perito, imgs[treino], 16,
                         fixo=torch.randn(500, CODIGO))
regua = [fatiada(x, referencia) for x in fotos]
print("época  perito  gerador  régua")
for epoca, ((p, g), r) in enumerate(zip(historico, regua), 1):
    print(f"{epoca:5d} {p:7.3f} {g:8.3f} {r:6.3f}")
melhor = min(range(16), key=lambda e: regua[e])
print(f"melhor época: {melhor + 1}; última: 16")
r = torch.tensor(regua)[3:]
for nome, coluna in (("perito", 0), ("gerador", 1)):
    perda = torch.tensor([h[coluna] for h in historico])[3:]
    c = torch.corrcoef(torch.stack([perda, r]))[0, 1]
    print(f"correlação com a régua, {nome}: {c:.2f}")

fig, (perdas, eixo_r) = plt.subplots(1, 2, figsize=(9, 3))
epocas = range(1, 17)
perdas.plot(epocas, [p for p, _ in historico], label="perito")
perdas.plot(epocas, [g for _, g in historico], label="gerador")
perdas.set_title("perdas", fontsize=9)
perdas.legend(fontsize=7)
eixo_r.plot(epocas, regua, color="C2")
eixo_r.set_title("régua: distância fatiada", fontsize=9)
for eixo in (perdas, eixo_r):
    eixo.set_xlabel("época")
fig.tight_layout()
fig.savefig("curvas_dcgan.png", dpi=300)
grade(torch.cat([fotos[e][:8] for e in (3, 7, 11, 15)]),
      "amostras_dcgan.png", 8)
