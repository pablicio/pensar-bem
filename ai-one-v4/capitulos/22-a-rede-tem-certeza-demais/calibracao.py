import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from leitora.calibra import erro_de_calibracao, por_faixa
from leitora.calibra import temperatura
from leitora.carrega import leitora
from leitora.dados import CaixasDoCartao

valid = CaixasDoCartao("validacao")
with torch.no_grad():
    logitos = leitora()(valid.imagens)
y = valid.rotulos

# trinta cartões ajustam a temperatura, trinta conferem
cartoes = list(dict.fromkeys(o[0] for o in valid.origem))
ajuste = torch.tensor([o[0] in cartoes[:30]
                       for o in valid.origem])
confere = ~ajuste

t = temperatura(logitos[ajuste], y[ajuste])
print(f"temperatura: {t:.3f}")
print(f"\n{'conferência':11} {'acerto':>7}"
      f" {'perda':>7} {'ECE':>6}")
fig, ax = plt.subplots(figsize=(4.5, 4.5))
ax.plot([0, 1], [0, 1], color="gray", linestyle=":")
versoes = [("sem ajuste", logitos),
           ("com ajuste", logitos / t)]
for nome, z in versoes:
    z, alvo = z[confere], y[confere]
    p = z.softmax(dim=1)
    acerto = (p.argmax(dim=1) == alvo).float().mean()
    perda = F.cross_entropy(z, alvo)
    ece = erro_de_calibracao(p, alvo)
    print(f"{nome:11} {acerto:7.2%} {perda:7.4f} {ece:6.2%}")
    faixas = por_faixa(p, alvo)
    ax.plot([f[3] for f in faixas], [f[4] for f in faixas],
            marker="o", label=nome)
ax.set_xlabel("confiança da rede")
ax.set_ylabel("acerto de verdade")
ax.legend()
fig.tight_layout()
fig.savefig("calibracao.png", dpi=400)

print()
for i, o in enumerate(valid.origem):
    if (o[0], o[1], o[2]) in [(38_259, 1, 1), (31_877, 8, 1)]:
        antes = logitos[i].softmax(dim=0).max()
        depois = (logitos[i] / t).softmax(dim=0).max()
        print(f"inscrição {o[0]}, questão {o[1] + 1}:"
              f" {antes:.1%} -> {depois:.1%}")
