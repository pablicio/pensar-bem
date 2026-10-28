"""Fotos do mundo real: defeitos de câmera e o filtro."""
import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFilter

from dados.camera import fundo
from folha.conjunto import DESVIO, MEDIA


def estraga(foto, tipo, s):
    """A foto (HWC, uint8, 128 px) com um defeito."""
    img = foto.astype(np.float32) / 255
    if tipo == "escura":            # noite, sem flash
        img = img * 0.25 + s.normal(0, 0.03, img.shape)
    elif tipo == "flash":           # estourada no centro
        y, x = np.mgrid[:128, :128]
        brilho = np.exp(-((x - 64) ** 2 + (y - 60) ** 2) / 900)
        img = img * 1.3 + 0.8 * brilho[..., None]
    elif tipo == "borrada":         # a mão tremeu
        p = Image.fromarray(foto)
        p = p.filter(ImageFilter.GaussianBlur(3))
        img = np.asarray(p).astype(np.float32) / 255
    elif tipo == "dedo":            # o polegar na lente
        p = Image.fromarray(foto)
        cx = s.integers(20, 108)
        ImageDraw.Draw(p).ellipse([cx - 40, 70, cx + 40, 170],
                                  fill=(214, 160, 130))
        p = p.filter(ImageFilter.GaussianBlur(2))
        img = np.asarray(p).astype(np.float32) / 255
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def nao_folha(s, tipo):
    """Uma foto sem folha: só o chão, ou um borrão colorido."""
    if tipo == "chão":
        img = fundo(s, str(s.choice(["terra", "folhagem"])))
    else:                           # o cachorro, digamos
        img = np.ones((256, 256, 3)) * s.uniform(0.2, 0.8, 3)
        img += 0.15 * s.normal(size=(256, 256, 3))
    img = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    return np.asarray(Image.fromarray(img).resize((128, 128),
                                                  Image.BOX))


def confere(foto):
    """O motivo para recusar a foto (HWC, uint8), ou None. Os
    limiares saem das fotos de treino: nenhuma é recusada."""
    img = foto.astype(np.float32) / 255
    if img.mean() < 0.12:
        return "escura demais"
    if (img.min(axis=2) > 0.9).mean() > 0.01:
        return "estourada"
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    if ((r > 0.6) & (r > g + 0.1) & (g > b)).mean() > 0.1:
        return "dedo na lente"
    c = img.mean(axis=2)            # o laplaciano: nitidez
    laplace = np.abs(4 * c[1:-1, 1:-1] - c[:-2, 1:-1]
                     - c[2:, 1:-1] - c[1:-1, :-2]
                     - c[1:-1, 2:])
    if laplace.mean() < 0.008:
        return "borrada"
    if ((g > r + 0.03) & (g > b)).mean() < 0.04:
        return "sem folha"
    return None


def tensores(fotos):
    """HWC uint8 → N × 3 × 128 × 128, normalizado."""
    x = torch.from_numpy(np.stack(fotos)).permute(0, 3, 1, 2)
    media = torch.tensor(MEDIA).view(1, 3, 1, 1)
    desvio = torch.tensor(DESVIO).view(1, 3, 1, 1)
    return (x.float() / 255 - media) / desvio
