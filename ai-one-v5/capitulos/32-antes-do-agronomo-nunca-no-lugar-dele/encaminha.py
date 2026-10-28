import torch

from folha.decisao import notas_fora_da_dobra, temperatura
from folha.emprestada import treina_cabeca

m = torch.load("caracteristicas.pt")
(xt, yt), (xv, yv) = m["treino"], m["validacao"]
notas_t = notas_fora_da_dobra(xt, yt)
T = temperatura(notas_t, yt)
cabeca = treina_cabeca(xt, yt)
with torch.no_grad():
    pv = (cabeca(xv) / T).softmax(dim=1)
pt = (notas_t / T).softmax(dim=1)


def cobertura(p, y, limiar):
    """Fração que o aplicativo decide sozinho, e o acerto."""
    conf, prevista = p.max(dim=1)
    sozinho = conf >= limiar
    acerto = (prevista[sozinho] == y[sozinho]).float().mean()
    return sozinho.float().mean().item(), acerto.item()


print("limiar  decide sozinho  acerto nelas  vai ao agrônomo")
for limiar in (0.0, 0.5, 0.7, 0.8, 0.9, 0.95):
    c, a = cobertura(pv, yv, limiar)
    print(f"{limiar:6.2f} {c:15.1%} {a:13.1%} {1 - c:16.1%}")

# o menor limiar com que, no treino, o automático acerta 95%
limiares = [t / 100 for t in range(50, 100)]
limiar = next(t for t in limiares
              if cobertura(pt, yt, t)[1] >= 0.95)
c, a = cobertura(pv, yv, limiar)
print(f"\nlimiar escolhido no treino: {limiar:.2f}")
print(f"na validação, decide {c:.1%} sozinho,"
      f" com {a:.1%} de acerto")
melhor = max(cobertura(pt, yt, t)[1] for t in limiares)
print(f"maior acerto no treino, com qualquer limiar:"
      f" {melhor:.1%}")
