import torch

from lauber.acervo import FAMILIAS, carrega, grade, partes
from lauber.autoencoder import Denso, treina
from lauber.classificador import Classificador
from lauber.classificador import treina as treina_juiz
from lauber.vae import VAE, treina_vae

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina_juiz(juiz, imgs[treino], familia[treino])
torch.manual_seed(0)
ae = Denso(codigo=16)           # o autoencoder do capítulo 5
treina(ae, imgs[treino], epocas=10)
torch.manual_seed(0)
vae = VAE(codigo=16, convolucional=True)
treina_vae(vae, imgs[treino], epocas=4)
vae.eval()
a = torch.linspace(0, 1, 8)[:, None]
with torch.no_grad():
    # da Rosa ao Xadrez, pelos dois códigos
    z0, z1 = ae.codificador(imgs[:2])
    pelo_ae = ae.decodificador((1 - a) * z0 + a * z1)
    (m0, m1), _ = vae.codifica(imgs[:2])
    pelo_vae = vae.decodificador((1 - a) * m0 + a * m1)
    # a direção "de listra para floral" no código do VAE
    mu, _ = vae.codifica(imgs[teste])
    f = familia[teste]
    direcao = mu[f == 3].mean(0) - mu[f == 0].mean(0)
    listra = mu[f == 0][:1]
    t = torch.linspace(0, 1.75, 8)[:, None]
    soma = vae.decodificador(listra + t * direcao)
    floral = juiz(soma).softmax(1)[:, 3]
print("t      ", " ".join(f"{x:5.2f}" for x in t[:, 0]))
print("floral?", " ".join(f"{p:5.0%}" for p in floral))
grade(torch.cat([pelo_ae, pelo_vae, soma]), "anda.png", 8)
