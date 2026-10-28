import torch

from lauber.acervo import carrega, partes
from lauber.classificador import Classificador, treina
from lauber.dcgan import CODIGO, Gerador, desenha
from lauber.medidas import (caracteristicas, frechet,
                            precisao_cobertura)
from lauber.vae import VAE, treina_vae

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina(juiz, imgs[treino], familia[treino])

torch.manual_seed(0)
vae = VAE(codigo=16, convolucional=True)   # o do capítulo 14
treina_vae(vae, imgs[treino], epocas=4)
vae.eval()
dcgan = Gerador()
dcgan.load_state_dict(torch.load("dcgan.pt"))

N = 1000
torch.manual_seed(1)
z = torch.randn(N, CODIGO)
with torch.no_grad():
    do_vae = vae.decodificador(torch.randn(N, 16))
candidatos = {
    "acervo (treino)": imgs[treino][:N],
    "DCGAN": desenha(dcgan, z),
    "DCGAN, um ruído só": desenha(dcgan,
                                  z[:1].expand(N, -1)),
    "VAE": do_vae,
    "ruído": torch.rand(N, 3, 32, 32),
}
reais = caracteristicas(juiz, imgs[teste][:N])
print("candidato           Fréchet  precisão  cobertura")
for nome, x in candidatos.items():
    f = caracteristicas(juiz, x)
    p, c = precisao_cobertura(reais, f)
    print(f"{nome:19} {frechet(reais, f):7.1f}"
          f" {p:9.0%} {c:10.0%}")
