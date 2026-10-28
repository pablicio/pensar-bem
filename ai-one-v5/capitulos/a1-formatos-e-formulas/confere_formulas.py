"""As fórmulas do apêndice A1 contra o PyTorch."""
import torch
from torch import nn

from folha.custo import multiplicacoes, parametros

sorteio = torch.Generator().manual_seed(5)


def sorteia(a, b):
    n = torch.randint(a, b + 1, (1,), generator=sorteio)
    return int(n)


def saida(n, k, s, p, d=1):
    return (n + 2 * p - d * (k - 1) - 1) // s + 1


def saida_transposta(m, k, s, p, e=0):
    return (m - 1) * s - 2 * p + k + e


casos = 0
NOMES = ["saída da convolução", "saída do pooling",
         "saída da transposta", "parâmetros", "multiplicações"]
erros = dict.fromkeys(NOMES, 0)
while casos < 300:
    n, k, s = sorteia(8, 40), sorteia(1, 7), sorteia(1, 3)
    p, d, g = sorteia(0, k // 2), sorteia(1, 2), sorteia(1, 3)
    c, sai = g * sorteia(1, 4), g * sorteia(1, 4)
    e = sorteia(0, s - 1)        # os extras da transposta
    o = saida(n, k, s, p, d)
    if o < 1:
        continue
    casos += 1
    x = torch.zeros(1, c, n, n)
    conv = nn.Conv2d(c, sai, k, s, p, d, groups=g)
    pool = nn.MaxPool2d(k, s, p)
    trans = nn.ConvTranspose2d(c, sai, k, s, p, e, groups=g)
    with torch.no_grad():
        erros["saída da convolução"] += conv(x).shape[-1] != o
        o_pool = saida(n, k, s, p)
        erros["saída do pooling"] += (
            pool(x).shape[-1] != o_pool)
        o_trans = saida_transposta(n, k, s, p, e)
        erros["saída da transposta"] += (
            trans(x).shape[-1] != o_trans)
    erros["parâmetros"] += (
        parametros(conv) != (k * k * c // g + 1) * sai)
    erros["parâmetros"] += (
        parametros(trans) != k * k * c * sai // g + sai)
    m = k * k * c // g * sai * o * o
    erros["multiplicações"] += multiplicacoes(conv, x) != m
print(f"{casos} camadas sorteadas")
for nome, n in erros.items():
    print(f"  {nome:22} {n} erros")


def campo(camadas):
    """r e j, camada a camada, como no capítulo 8."""
    r, j = 1, 1
    for k, s in camadas:
        r, j = r + (k - 1) * j, j * s
    return r


def campo_medido(camadas, n=129):
    """Os pixels da entrada que mexem no pixel do meio."""
    pecas = [nn.Conv2d(1, 1, k, s, bias=False)
             for k, s in camadas]
    for peca in pecas:
        nn.init.ones_(peca.weight)
    x = torch.zeros(1, 1, n, n, requires_grad=True)
    y = nn.Sequential(*pecas)(x)
    meio = y.shape[-1] // 2
    y[0, 0, meio, meio].backward()
    linhas = x.grad[0, 0].sum(dim=1).nonzero()
    return int(linhas.max() - linhas.min() + 1)


PILHAS = [[(3, 1)] * 3,
          [(3, 1), (2, 2), (3, 1), (2, 2), (3, 1)],
          [(5, 1), (2, 2), (5, 1), (2, 2)],
          [(7, 2), (3, 2), (3, 1), (3, 1), (3, 2), (3, 1)]]
print("campo receptivo (núcleo/passo): fórmula, medido")
for pilha in PILHAS:
    texto = " ".join(f"{k}/{s}" for k, s in pilha)
    r, medido = campo(pilha), campo_medido(pilha)
    print(f"  {texto:24} {r:3} {medido:3}")

C, S = 64, 128
cheia = nn.Conv2d(C, S, 3, padding=1, bias=False)
separavel = nn.Sequential(
    nn.Conv2d(C, C, 3, padding=1, groups=C, bias=False),
    nn.Conv2d(C, S, 1, bias=False))
razao = parametros(separavel) / parametros(cheia)
print(f"separável/cheia: {razao:.4f};"
      f" 1/S + 1/9 = {1 / S + 1 / 9:.4f}")
