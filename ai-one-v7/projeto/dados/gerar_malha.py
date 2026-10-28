"""Gera fotos de malha de jérsei, boas e com defeito, em tons
de cinza, com a máscara de cada defeito."""
from pathlib import Path

import numpy as np

PASTA = Path("dados/brutos")
# artigo: (tom do fio, contraste das laçadas, pintas da mescla)
ARTIGOS = {"preta": (0.15, 0.10, 0.0),
           "branca": (0.85, 0.10, 0.0),
           "azul": (0.40, 0.12, 0.0),
           "mescla": (0.55, 0.10, 0.25)}
DEFEITOS = ["furo", "agulha", "mancha"]


def malha(sorteio, artigo, n=32):
    """As laçadas em V do jérsei, com o fio irregular."""
    tom, contraste, mescla = ARTIGOS[artigo]
    y, x = np.mgrid[0:n, 0:n].astype(float)
    fase = sorteio.uniform(0, 4, 2)
    v = np.abs(((x + fase[1]) / 4) % 1 - 0.5)
    lacada = np.cos(2 * np.pi * ((y + fase[0]) / 4 + v))
    img = tom + contraste * lacada
    img += sorteio.normal(0, 0.02, (n, n))
    if mescla:                       # fibras claras e escuras
        img += mescla * (sorteio.random((n, n)) - 0.5)
    return img


def defeito(sorteio, img, tipo):
    """O defeito e a máscara de onde ele está."""
    img, n = img.copy(), img.shape[0]
    y, x = np.mgrid[0:n, 0:n]
    cy, cx = sorteio.integers(6, n - 6, 2)
    if tipo == "furo":
        raio = sorteio.uniform(2, 4)
        mascara = np.hypot(y - cy, x - cx) < raio
        img[mascara] = 0.02                  # o fundo escuro
    elif tipo == "agulha":           # uma coluna sem laçada
        mascara = np.abs(x - cx) < 1
        img[mascara] = img.mean() + 0.25
    else:                                    # óleo: escurece
        raio = sorteio.uniform(3, 6)
        peso = np.exp(-((y - cy) ** 2 + (x - cx) ** 2)
                      / (2 * raio ** 2))
        img = img * (1 - 0.6 * peso)
        mascara = peso > 0.3
    return img, mascara


def lote(sorteio, artigos, quantos, tipo=None):
    imgs, mascaras, nomes = [], [], []
    for _ in range(quantos):
        artigo = str(sorteio.choice(artigos))
        img = malha(sorteio, artigo)
        mascara = np.zeros(img.shape, bool)
        if tipo:
            img, mascara = defeito(sorteio, img, tipo)
        imgs.append(np.clip(img, 0, 1))
        mascaras.append(mascara)
        nomes.append(artigo)
    return imgs, mascaras, nomes


def main(semente=11):
    sorteio = np.random.default_rng(semente)
    do_treino = ["preta", "branca", "azul"]
    partes = {"treino": lote(sorteio, do_treino, 6_000)}
    imgs, mascaras, artigos, tipos = [], [], [], []
    for tipo in [None] + DEFEITOS:
        quantos = 2_000 if tipo is None else 40
        i, m, a = lote(sorteio, do_treino, quantos, tipo)
        imgs += i
        mascaras += m
        artigos += a
        tipos += [tipo or "bom"] * quantos
    PASTA.mkdir(parents=True, exist_ok=True)
    treino, _, art_treino = partes["treino"]
    np.savez_compressed(
        PASTA / "malha.npz",
        treino=np.array(treino, np.float32),
        artigo_treino=np.array(art_treino),
        teste=np.array(imgs, np.float32),
        mascara_teste=np.array(mascaras),
        artigo_teste=np.array(artigos),
        tipo_teste=np.array(tipos))
    print(len(treino), "fotos de treino,", len(imgs),
          "de teste")


if __name__ == "__main__":
    main()
