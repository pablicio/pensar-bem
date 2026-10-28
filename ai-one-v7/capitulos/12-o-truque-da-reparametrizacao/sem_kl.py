import torch

from lauber.acervo import carrega, partes
from lauber.vae import VAE, treina_vae

torch.manual_seed(0)
imgs, _ = carrega()
treino, _, teste = partes(len(imgs))
rede = VAE(codigo=2)
for epoca in range(7):
    if epoca > 0:     # beta = 0: só a reconstrução, sem a KL
        treina_vae(rede, imgs[treino], epocas=1, beta=0.0)
    with torch.no_grad():
        mu, logvar = rede.codifica(imgs[teste])
    sigma = torch.exp(0.5 * logvar)
    print(f"época {epoca}: raio médio {sigma.mean():.4f},"
          f" espalhamento {mu.std(dim=0).mean():.2f}")
