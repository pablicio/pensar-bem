import torch

from folha.conjunto import Folhas
from folha.emprestada import extrai, extratora, treina_cabeca
from folha.treino import fixar_semente

fixar_semente(0, nucleos=4)
xt, yt = torch.load("caracteristicas.pt")["treino"]
cabeca = treina_cabeca(xt, yt)
teste = Folhas("teste")        # aberto pela primeira vez
xs, ys = extrai(extratora(), teste)
with torch.no_grad():
    certo = (cabeca(xs).argmax(dim=1) == ys).float()
fazendas = [f["fazenda"] for f in teste.linhas]
nomes = sorted(set(fazendas))
print(f"teste: {len(ys)} fotos de {len(nomes)} fazendas;"
      f" acerto {certo.mean():.1%}")
por_fazenda = []
for nome in nomes:
    dela = torch.tensor([f == nome for f in fazendas])
    acerto = certo[dela].mean()
    por_fazenda.append(acerto)
    print(f"  {nome}: {dela.sum():3} fotos, {acerto:.1%}")
por_fazenda = torch.stack(por_fazenda)

sorteador = torch.Generator().manual_seed(34)
B = 5000
fotos = torch.randint(len(certo), (B, len(certo)),
                      generator=sorteador)
por_foto = certo[fotos].mean(dim=1)         # sorteia fotos
idx = torch.randint(len(nomes), (B, len(nomes)),
                    generator=sorteador)
por_faz = por_fazenda[idx].mean(dim=1)      # sorteia fazendas
doze = torch.randint(len(nomes), (B, 12), generator=sorteador)
doze = por_fazenda[doze].mean(dim=1)       # 12 com reposição
for nome, amostras in (("sorteando fotos", por_foto),
                       ("sorteando fazendas", por_faz),
                       ("12 fazendas da exportadora", doze)):
    pontas = torch.tensor([0.025, 0.975])
    baixo, alto = amostras.quantile(pontas)
    print(f"95% {nome:27} {baixo:.1%} a {alto:.1%}")

desvio = por_fazenda.std()
for margem in (0.03, 0.02, 0.01):
    n = (1.96 * desvio / margem) ** 2
    print(f"fazendas para ±{margem:.0%}: {n.ceil():.0f}")
