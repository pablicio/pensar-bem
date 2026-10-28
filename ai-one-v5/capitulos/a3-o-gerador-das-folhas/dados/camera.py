"""A câmera: põe a folha sobre um fundo e fotografa."""
import numpy as np
from PIL import Image, ImageFilter

from dados.desenho import L, ruido, suave


def fundo(s, tipo):
    """O que está atrás da folha."""
    if tipo == "terra":
        cor = np.array([105, 78, 55]) / 255
        img = cor * s.uniform(0.85, 1.15) \
            + 0.10 * ruido(s, 6)[..., None] \
            + 0.05 * ruido(s, 2)[..., None]
    elif tipo == "folhagem":       # folhas fora de foco
        img = np.array([30, 60, 28]) / 255 \
            + 0.12 * ruido(s, 24)[..., None] \
            * np.array([0.6, 1.0, 0.5])
    elif tipo == "mesa":           # a bancada do laboratório
        img = np.array([62, 112, 178]) / 255 \
            + 0.025 * ruido(s, 40)[..., None]
    else:
        raise ValueError(tipo)
    return np.clip(img * np.ones((L, L, 3)), 0, 1)


def afim(angulo, escala, desloc):
    """Matriz A e vetor b: saída = A · entrada + b."""
    a = np.deg2rad(angulo)
    A = escala * np.array([[np.cos(a), np.sin(a)],
                           [-np.sin(a), np.cos(a)]])
    centro = np.array([L / 2, L / 2])
    b = centro + np.asarray(desloc) - A @ centro
    return A, b


def transforma(arr, A, b, metodo):
    """Aplica a afim; o Pillow pede o mapa inverso."""
    inv = np.linalg.inv(A)
    c = -inv @ b
    coef = (*inv[0], c[0], *inv[1], c[1])
    img = Image.fromarray(arr)
    img = img.transform((L, L), Image.AFFINE, coef,
                        resample=metodo)
    return np.array(img)


def fotografa(desenho, s, tipo_fundo, angulo=0.0, escala=1.0,
              desloc=(0, 0), luz=1.0, tons=(1.0, 1.0, 1.0)):
    """A foto, as máscaras e os pontos transformados."""
    A, b = afim(angulo, escala, desloc)
    rgba = np.dstack([desenho["cor"], desenho["alfa"]])
    rgba = (rgba * 255).astype(np.uint8)
    rgba = transforma(rgba, A, b, Image.BICUBIC) / 255
    ids = np.zeros((L, L), np.uint8)       # 0 é sem lesão
    for k, m in enumerate(desenho["lesoes"], 1):
        ids[m] = k
    ids = transforma(ids, A, b, Image.NEAREST)
    alfa = rgba[..., 3:]

    img = fundo(s, tipo_fundo)
    sombra = np.roll(suave(alfa[..., 0], 5), (6, 5), (0, 1))
    img *= 1 - 0.35 * sombra[..., None]
    img = img * (1 - alfa) + rgba[..., :3] * alfa
    img = img * luz * np.array(tons)
    img += s.normal(0, s.uniform(0.008, 0.02), img.shape)
    img = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    desfoque = ImageFilter.GaussianBlur(s.uniform(0, 0.7))
    foto = Image.fromarray(img).filter(desfoque)

    # máscara: 0 fundo, 1 folha, 2 lesão
    mascara = (alfa[..., 0] > 0.5).astype(np.uint8)
    mascara[(ids > 0) & (mascara == 1)] = 2
    ids[mascara != 2] = 0
    pontos = [A @ np.array(desenho[k]) + b
              for k in ("ponta", "peciolo")]
    return np.asarray(foto), mascara, ids, pontos
