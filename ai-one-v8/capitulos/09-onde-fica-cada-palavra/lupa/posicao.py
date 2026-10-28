"""Três jeitos de dizer onde fica cada token."""
import torch


def frequencias(d, base=10000.0):
    """ω_i = base^(-2i/d), uma para cada par de dimensões."""
    return base ** (-torch.arange(0, d, 2) / d)


def senoidal(T, d):
    """PE(t, 2i) = sen(t ω_i), PE(t, 2i+1) = cos(t ω_i)."""
    angulos = torch.arange(T)[:, None] * frequencias(d)
    pe = torch.zeros(T, d)
    pe[:, 0::2] = torch.sin(angulos)
    pe[:, 1::2] = torch.cos(angulos)
    return pe


def rope(x):
    """Gira cada par de dimensões do token t pelo ângulo t ω_i.
    x: (..., T, d), com d par."""
    T, d = x.shape[-2], x.shape[-1]
    angulos = torch.arange(T)[:, None] * frequencias(d)
    c, s = torch.cos(angulos), torch.sin(angulos)
    a, b = x[..., 0::2], x[..., 1::2]     # os pares (a, b)
    girado = torch.stack([a * c - b * s, a * s + b * c],
                         dim=-1)
    return girado.flatten(-2)             # volta a intercalar
