import matplotlib.pyplot as plt
import torch

from lupa.corpus import prepara
from lupa.gpt import GPT

tok, treino, teste = prepara()
modelo = GPT(len(tok.vocab))
modelo.load_state_dict(torch.load("gpt.pt"))
modelo.eval()

# 2027 em janelas de 128 tokens, sem sobreposição
n = (len(teste) - 1) // 128
x = teste[:n * 128].view(n, 128)
y = teste[1:n * 128 + 1].view(n, 128)
with torch.no_grad():
    p = torch.cat([modelo(x[i:i + 64]).softmax(-1)
                   for i in range(0, n, 64)])
confianca, palpite = p.max(-1)
acerto = (palpite == y).float()
confianca, acerto = confianca.flatten(), acerto.flatten()
print(f"{len(acerto)} previsões, acerto {acerto.mean():.3f},"
      f" confiança média {confianca.mean():.3f}")

print("faixa       previsões")
bordas = torch.linspace(0, 1, 11)
ece, pontos = 0.0, []
for a, b in zip(bordas[:-1], bordas[1:]):
    dentro = (confianca > a) & (confianca <= b)
    if dentro.sum() == 0:
        continue
    c, ac = confianca[dentro].mean(), acerto[dentro].mean()
    peso = dentro.float().mean()
    ece += peso * (ac - c).abs()
    pontos.append((c.item(), ac.item()))
    print(f"  ({a:.1f}, {b:.1f}]  {100 * peso:5.1f}%"
          f"  confiança {c:.3f}  acerto {ac:.3f}")
print(f"erro de calibração esperado: {ece:.4f}")

fig, eixo = plt.subplots(figsize=(4, 4))
eixo.plot([0, 1], [0, 1], "--", color="gray")
eixo.plot(*zip(*pontos), "o-")
eixo.set_xlabel("confiança (probabilidade do palpite)")
eixo.set_ylabel("fração de acertos")
fig.tight_layout()
fig.savefig("calibracao.png", dpi=400)
