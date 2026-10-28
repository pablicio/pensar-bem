import matplotlib.pyplot as plt
import torch

from lupa.corpus import prepara
from lupa.gpt import GPT

tok, treino, teste = prepara()
modelo = GPT(len(tok.vocab))
modelo.load_state_dict(torch.load("gpt.pt"))
modelo.eval()

# os logits do token que vem depois de "Objeto:"
x = torch.tensor([tok.codifica(
    "<|fim|>EXTRATO DO CONTRATO Nº 012/2026\nContratante:"
    " Município de Alto Bonito. Objeto:")])
with torch.no_grad():
    z = modelo(x)[0, -1].double()


def entropia(T):
    """Em nats: H = -soma p log p, com p = softmax(z / T)."""
    logp = torch.log_softmax(z / T, -1)
    return -(logp.exp() * logp).sum().item()


for T in [0.5, 1.0, 2.0]:
    p = torch.softmax(z / T, -1)
    var = (p * z ** 2).sum() - (p * z).sum() ** 2
    formula = var.item() / T ** 3
    h = 1e-5
    finita = (entropia(T + h) - entropia(T - h)) / (2 * h)
    print(f"T = {T}: H = {entropia(T):.3f} nats,"
          f" dH/dT = {finita:.4f} (fórmula {formula:.4f})")

print("os cinco mais prováveis a T = 1:")
p = torch.softmax(z, -1)
for prob, i in zip(*p.topk(5)):
    print(f"  {prob.item():.3f} {tok.mostra(i.item())}")

Ts = torch.logspace(-1.5, 1, 100)
fig, eixo = plt.subplots(figsize=(6, 3))
eixo.semilogx(Ts, [entropia(T.item()) for T in Ts])
eixo.axhline(torch.log(torch.tensor(len(z))).item(),
             ls="--", color="gray", label="ln V (uniforme)")
eixo.set_xlabel("temperatura T")
eixo.set_ylabel("entropia (nats)")
eixo.legend()
fig.tight_layout()
fig.savefig("temperatura.png", dpi=300)
