import matplotlib.pyplot as plt
import torch

from folha.decisao import ece, notas_fora_da_dobra, temperatura
from folha.emprestada import treina_cabeca

m = torch.load("caracteristicas.pt")
(xt, yt), (xv, yv) = m["treino"], m["validacao"]
T = temperatura(notas_fora_da_dobra(xt, yt), yt)   # só treino
cabeca = treina_cabeca(xt, yt)
with torch.no_grad():
    notas = cabeca(xv)
antes = notas.softmax(dim=1)
depois = (notas / T).softmax(dim=1)
VERSOES = (("sem ajuste", antes), ("com temperatura", depois))
print(f"temperatura escolhida no treino: {T:.2f}")
for nome, p in VERSOES:
    conf = p.max(dim=1).values.mean()
    print(f"{nome:16} confiança média {conf:.3f};"
          f" ECE {ece(p, yv):.3f}")
acerto = (notas.argmax(dim=1) == yv).float().mean()
print(f"acerto (igual nos dois): {acerto:.3f}")

fig, ax = plt.subplots(figsize=(4.2, 4))
for nome, p in VERSOES:
    conf, prevista = p.max(dim=1)
    certo = (prevista == yv).float()
    xs, ys = [], []
    for i in range(10):
        dentro = (conf > i / 10) & (conf <= (i + 1) / 10)
        if dentro.sum() >= 5:
            xs.append(conf[dentro].mean())
            ys.append(certo[dentro].mean())
    ax.plot(xs, ys, marker="o", label=nome)
ax.plot([0, 1], [0, 1], color="gray", ls="--")
ax.set_xlabel("confiança média da faixa")
ax.set_ylabel("acerto na faixa")
ax.legend()
fig.tight_layout()
fig.savefig("calibracao.png", dpi=400)
