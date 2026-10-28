"""Gera o acervo da Lauber, os danos do escaneamento e o
catálogo de um concorrente. Tudo com semente."""
from pathlib import Path

import numpy as np

from dados.estampas import FAMILIAS, PALETAS, desenha

PASTA = Path("dados/brutos")
N, ZULEICA = 14_000, 2_300
DECADAS = list(PALETAS)


def danifica(sorteio, img):
    """Mofo, dobra ou mancha: o que o tempo fez na gaveta."""
    img, n = img.copy(), img.shape[0]
    dano = str(sorteio.choice(["mofo", "dobra", "mancha"]))
    y, x = np.mgrid[0:n, 0:n] / n
    if dano == "mofo":                  # pintas acinzentadas
        for _ in range(int(sorteio.integers(3, 8))):
            cy, cx = sorteio.uniform(0, 1, 2)
            raio = sorteio.uniform(0.02, 0.06)
            pinta = np.hypot(y - cy, x - cx) < raio
            img[pinta] = 0.5 * img[pinta] + 0.5 * np.array(
                [.45, .5, .4])
    elif dano == "dobra":               # uma linha mais clara
        a = sorteio.uniform(-0.3, 0.3)
        b = sorteio.uniform(0.2, 0.8)
        linha = np.abs(y - (a * x + b)) < 0.03
        img[linha] = np.minimum(img[linha] + 0.35, 1.0)
    else:                               # uma mancha amarelada
        cy, cx = sorteio.uniform(0.2, 0.8, 2)
        peso = np.exp(-((y - cy) ** 2 + (x - cx) ** 2) / 0.02)
        img = img * (1 - 0.6 * peso[..., None]) + 0.6 * peso[
            ..., None] * np.array([.85, .75, .45])
    return np.clip(img, 0, 1), dano


def erro_proposital(sorteio, img):
    """A Zuleica errava de propósito: um pedaço sem motivo."""
    img, n = img.copy(), img.shape[0]
    y, x = sorteio.integers(0, n - 6, 2)
    img[y:y + 6, x:x + 6] = img[0, 0]       # a cor do fundo
    return img


def bytes8(imgs):
    return np.round(np.array(imgs) * 255).astype(np.uint8)


def acervo(sorteio):
    linhas, limpas, escaneadas = [], [], []
    for i in range(N):
        zuleica = i < ZULEICA
        fim = 2000 if zuleica else 2027
        ano = int(sorteio.integers(1961, fim))
        familia = int(sorteio.integers(len(FAMILIAS)))
        mao = sorteio.uniform(0.03, 0.06) if zuleica else 0.02
        img = desenha(sorteio, familia, ano // 10 * 10, mao)
        proposital = zuleica and sorteio.random() < 0.3
        if proposital:
            img = erro_proposital(sorteio, img)
        dano = ""
        if sorteio.random() < 0.5:
            escaneada, dano = danifica(sorteio, img)
        else:
            escaneada = img
        limpas.append(img)
        escaneadas.append(escaneada)
        linhas.append((ano, familia, zuleica, proposital,
                       dano))
    ano, familia, zuleica, proposital, dano = zip(*linhas)
    return dict(limpa=bytes8(limpas),
                escaneada=bytes8(escaneadas),
                ano=np.array(ano), familia=np.array(familia),
                zuleica=np.array(zuleica),
                proposital=np.array(proposital),
                dano=np.array(dano))


def especiais(dados):
    """A Rosa de 1964 e o Xadrez de 1971, nos lugares 0 e 1."""
    for lugar, (semente, familia, ano) in enumerate(
            [(1964, 3, 1964), (1971, 1, 1971)]):
        img = desenha(np.random.default_rng(semente), familia,
                      ano // 10 * 10, 0.04)
        dados["limpa"][lugar] = dados["escaneada"][lugar] = \
            bytes8([img])[0]
        dados["ano"][lugar] = ano
        dados["familia"][lugar] = familia
        dados["dano"][lugar] = ""


def catalogo(sorteio, n=3_000):
    """O catálogo de outra estamparia, de 2019, e as três
    'originais' da Synapsys: três dele, espelhadas e
    retocadas."""
    imgs = [desenha(sorteio, int(sorteio.integers(6)),
                    int(sorteio.choice(DECADAS[3:])), 0.02)
            for _ in range(n)]
    escolhidas = sorteio.choice(n, size=3, replace=False)
    synapsys = [np.clip(imgs[i][:, ::-1] * 0.95 + 0.03, 0, 1)
                for i in escolhidas]
    return bytes8(imgs), bytes8(synapsys), escolhidas


def main(semente=7):
    sorteio = np.random.default_rng(semente)
    dados = acervo(sorteio)
    especiais(dados)
    cat, syn, origem = catalogo(sorteio)
    PASTA.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(PASTA / "acervo.npz", **dados)
    np.savez_compressed(PASTA / "catalogo.npz", imagens=cat)
    np.savez_compressed(PASTA / "synapsys.npz", imagens=syn,
                        origem=origem)
    print(len(dados["limpa"]), "estampas no acervo,",
          len(cat), "no catálogo")


if __name__ == "__main__":
    main()
