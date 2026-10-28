import matplotlib.pyplot as plt
import torch

from leitora.carrega import leitora
from leitora.dados import CaixasDoCartao
from leitora.decide import decide

valid = CaixasDoCartao("validacao")
with torch.no_grad():
    logitos = leitora()(valid.imagens)

# os trinta cartões que não escolheram a temperatura
cartoes = list(dict.fromkeys(o[0] for o in valid.origem))
confere = torch.tensor([o[0] in cartoes[30:]
                        for o in valid.origem])
logitos, y = logitos[confere], valid.rotulos[confere]

print(f"{'limiar':>7} {'lê':>6} {'revisa':>7}"
      f" {'erros contados':>15} {'esperados':>10}")
for lim in [0, 0.5, 0.8, 0.9, 0.95, 0.99, 0.995, 0.999]:
    leitura, confianca, le = decide(logitos, lim)
    contados = (leitura[le] != y[le]).sum()
    esperados = (1 - confianca[le]).sum()
    revisa = int((~le).sum())
    print(f"{lim:7.3f} {le.float().mean():6.1%} {revisa:7}"
          f" {contados:15} {esperados:10.1f}")

# a curva inteira: cobertura contra erro entre as lidas
leitura, confianca, _ = decide(logitos, 0)
ordem = confianca.argsort(descending=True)
erro = (leitura[ordem] != y[ordem]).float()
k = torch.arange(1, len(y) + 1)
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(k / len(y), erro.cumsum(0) / k, label="contado")
ax.plot(k / len(y), (1 - confianca[ordem]).cumsum(0) / k,
        linestyle="--", label="esperado")
ax.set_xlabel("fração das caixas que a rede lê sozinha")
ax.set_ylabel("erro entre as lidas")
ax.legend()
fig.tight_layout()
fig.savefig("cobertura.png", dpi=300)
