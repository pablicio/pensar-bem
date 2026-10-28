import matplotlib.pyplot as plt
import torch

from lauber.acervo import carrega, grade, partes
from lauber.dcgan import CODIGO, Gerador, inicia
from lauber.wgan import Critico, fatiada, treina

imgs, _ = carrega()
treino, _, teste = partes(len(imgs))
referencia = imgs[teste][:500]
torch.manual_seed(0)
gerador, critico = Gerador(), Critico()
gerador.apply(inicia)
critico.apply(inicia)
fotos, historico = treina(gerador, critico, imgs[treino], 16,
                         jogo="wgan",
                         fixo=torch.randn(500, CODIGO))
regua = [fatiada(x, referencia) for x in fotos]
print("época  estimativa  régua")
for epoca, ((w, _), r) in enumerate(zip(historico, regua), 1):
    print(f"{epoca:5d} {w:11.1f} {r:6.3f}")
w = torch.tensor([w for w, _ in historico])
r = torch.tensor(regua)
correlacao = torch.corrcoef(torch.stack([w[3:], r[3:]]))[0, 1]
print(f"correlação, épocas 4 a 16: {correlacao:.2f}")

fig, eixo = plt.subplots(figsize=(4.5, 3))
eixo.plot(range(1, 17), w, label="estimativa do crítico")
eixo.set_xlabel("época")
outro = eixo.twinx()
outro.plot(range(1, 17), regua, color="C2", label="régua")
eixo.legend(loc="upper right", fontsize=7)
outro.legend(loc="center right", fontsize=7)
fig.tight_layout()
fig.savefig("curvas_wgan.png", dpi=400)
grade(torch.cat([fotos[e][:8] for e in (3, 7, 11, 15)]),
      "amostras_wgan.png", 8)
