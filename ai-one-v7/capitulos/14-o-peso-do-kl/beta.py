import torch

from lauber.acervo import carrega, grade, partes
from lauber.vae import VAE, treina_vae

BETAS = (0.1, 1, 4, 16, 64)
imgs, _ = carrega()
treino, _, teste = partes(len(imgs))
torch.manual_seed(1)
priori = torch.randn(8, 16)    # os mesmos 8 códigos
linhas = []
print(" beta  erro/pixel   KL  ativos  contraste")
for beta in BETAS:
    torch.manual_seed(0)
    rede = VAE(codigo=16, convolucional=True)
    historico = treina_vae(rede, imgs[treino], epocas=4,
                           beta=beta)
    rede.eval()
    with torch.no_grad():
        mu, logvar = rede.codifica(imgs[teste])
        rec = rede.decodificador(mu)
        amostras = rede.decodificador(priori)
    erro = ((rec - imgs[teste]) ** 2).mean()
    # a KL de cada um dos 16 números, na média do teste
    por_numero = 0.5 * (mu ** 2 + logvar.exp() - logvar
                        - 1).mean(dim=0)
    ativos = int((por_numero > 0.05).sum())
    contraste = amostras.std(dim=(2, 3)).mean()
    print(f"{beta:5} {erro:11.4f} {historico[-1][1]:6.2f}"
          f" {ativos:6d} {contraste:10.3f}")
    linhas.append(amostras)
print(f"contraste das estampas reais:"
      f" {imgs[teste].std(dim=(2, 3)).mean():.3f}")
grade(torch.cat(linhas), "beta.png", colunas=8)
