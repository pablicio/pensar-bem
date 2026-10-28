"""Dígitos como saem de uma página escaneada, em 32 x 32."""
import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFilter, ImageFont


def digito(d, rng):
    """O dígito d, desenhado, torto, borrado e com sujeira."""
    img = Image.new("L", (32, 32), 0)
    tamanho = int(rng.integers(18, 27))
    fonte = ImageFont.load_default(size=tamanho)
    x, y = int(rng.integers(6, 12)), int(rng.integers(0, 6))
    ImageDraw.Draw(img).text((x, y), str(d), fill=255,
                             font=fonte)
    img = img.rotate(float(rng.uniform(-12, 12)))
    borrao = ImageFilter.GaussianBlur(rng.uniform(0, 1.2))
    a = np.asarray(img.filter(borrao), dtype=np.float32) / 255
    a = a + rng.normal(0, 0.25, a.shape)          # o ruído
    return np.clip(a, 0, 1).astype(np.float32)


def conjunto(n, semente):
    """n dígitos sorteados: imagens (n, 1, 32, 32), rótulos."""
    rng = np.random.default_rng(semente)
    y = rng.integers(0, 10, n)
    x = np.stack([digito(d, rng) for d in y])[:, None]
    return torch.tensor(x), torch.tensor(y)
