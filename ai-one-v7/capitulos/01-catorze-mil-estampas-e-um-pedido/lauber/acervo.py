"""O acervo como tensores, a divisão e a grade de imagens."""
import matplotlib.pyplot as plt
import numpy as np
import torch

from dados.estampas import FAMILIAS

ARQUIVO = "dados/brutos/acervo.npz"


def carrega(versao="escaneada"):
    """As estampas (N, 3, 32, 32) de 0 a 1 e as informações."""
    dados = np.load(ARQUIVO)
    imgs = torch.tensor(dados[versao]).permute(0, 3, 1, 2)
    info = {k: dados[k] for k in dados.files
            if k not in ("limpa", "escaneada")}
    return imgs.float() / 255, info


def partes(n, semente=0):
    """Índices de treino (80%), validação e teste (10%)."""
    ordem = np.random.default_rng(semente).permutation(n)
    a, b = int(0.8 * n), int(0.9 * n)
    return ordem[:a], ordem[a:b], ordem[b:]


def grade(imgs, arquivo, colunas=8, titulos=None):
    """Grava uma grade de imagens (N, C, H, W) num PNG."""
    imgs = imgs.detach().clamp(0, 1)
    imgs = imgs.permute(0, 2, 3, 1).numpy()
    linhas = int(np.ceil(len(imgs) / colunas))
    fig, eixos = plt.subplots(linhas, colunas, squeeze=False,
                              figsize=(colunas, linhas * 1.1))
    for i, eixo in enumerate(eixos.flat):
        eixo.axis("off")
        if i < len(imgs):
            cinza = imgs[i].shape[2] == 1
            eixo.imshow(imgs[i].squeeze(), cmap="gray" if cinza
                        else None, vmin=0, vmax=1)
            if titulos is not None:
                eixo.set_title(titulos[i], fontsize=7)
    fig.tight_layout()
    # grades estreitas ganham mais pontos por polegada
    fig.savefig(arquivo, dpi=300 * max(1, 8 // colunas))
    plt.close(fig)


__all__ = ["FAMILIAS", "carrega", "partes", "grade"]
