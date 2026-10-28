import matplotlib.pyplot as plt
import torch

from folha.conjunto import CLASSES, DESVIO, MEDIA, Folhas
from folha.emprestada import Renormaliza, extratora
from folha.emprestada import treina_cabeca
from folha.treino import fixar_semente

fixar_semente(0, nucleos=4)
xt, yt = torch.load("caracteristicas.pt")["treino"]
cabeca = treina_cabeca(xt, yt)
rede = extratora()
r = rede[1]
for p in rede.parameters():
    p.requires_grad_(False)
valid = Folhas("validacao")


def primeira(classe):
    """A primeira foto da classe sobre a terra."""
    for i, f in enumerate(valid.linhas):
        if f["verdade"] == classe and f["fundo"] == "terra":
            return valid[i][0]


def camadas(x):
    """Os mapas de três estágios da ResNet-18."""
    x = Renormaliza()(x)
    x = r.maxpool(r.relu(r.bn1(r.conv1(x))))
    a = r.layer1(x)
    b = r.layer2(a)
    return [a, b, r.layer3(b)]


def gram(m):
    """A matriz de Gram: correlação entre os canais, C × C."""
    n, c, h, w = m.shape
    f = m.reshape(c, h * w)
    return f @ f.T / (h * w)


def classe(x):
    with torch.no_grad():
        p = cabeca(rede(x[None])).softmax(dim=1)[0]
    return f"{CLASSES[p.argmax()]} {p.max():.0%}"


conteudo, estilo = primeira("sadia"), primeira("ferrugem")
alvo_c = [m.detach() for m in camadas(conteudo[None])]
alvo_e = [gram(m).detach() for m in camadas(estilo[None])]
imagem = conteudo.clone()[None].requires_grad_(True)
otimizador = torch.optim.Adam([imagem], lr=0.03)
for passo in range(300):
    otimizador.zero_grad()
    mapas = camadas(imagem)
    perda_c = (mapas[2] - alvo_c[2]).pow(2).mean()
    perda_e = sum((gram(m) - g).pow(2).mean()
                  for m, g in zip(mapas, alvo_e))
    (perda_c + 1e3 * perda_e).backward()
    otimizador.step()
resultado = imagem.detach()[0]
for nome, x in (("sadia (conteúdo)", conteudo),
                ("ferrugem (estilo)", estilo),
                ("sadia com a textura", resultado)):
    print(f"{nome:20} a rede diz: {classe(x)}")

media = torch.tensor(MEDIA).view(3, 1, 1)
desvio = torch.tensor(DESVIO).view(3, 1, 1)
fig, eixos = plt.subplots(1, 3, figsize=(7, 2.6))
for ax, x, t in zip(eixos, (conteudo, estilo, resultado),
                    ("conteúdo: sadia", "estilo: ferrugem",
                     "resultado")):
    tela = (x * desvio + media).clamp(0, 1)
    ax.imshow(tela.permute(1, 2, 0))
    ax.set_title(t, fontsize=8)
    ax.axis("off")
fig.tight_layout()
fig.savefig("estilo.png", dpi=300)
