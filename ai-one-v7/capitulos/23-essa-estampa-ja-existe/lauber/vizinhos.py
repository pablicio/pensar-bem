"""Procurar a estampa mais parecida, com espelho ou sem."""
import numpy as np
import torch


def carrega_npz(nome):
    """As imagens de dados/brutos/<nome>.npz, de 0 a 1."""
    dados = np.load(f"dados/brutos/{nome}.npz")
    imgs = torch.tensor(dados["imagens"]).permute(0, 3, 1, 2)
    return imgs.float() / 255


def normaliza(imgs):
    """Cada estampa sem a própria média e com tamanho 1: o
    produto de duas é a correlação entre os pixels delas,
    que não muda com brilho nem com contraste."""
    x = imgs.flatten(1).double().numpy()
    x = x - x.mean(axis=1, keepdims=True)
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def vizinho(consulta, base, espelho=False):
    """Para cada estampa da consulta, o índice da mais
    parecida na base e a correlação entre as duas. Com
    `espelho`, vale também a consulta espelhada."""
    b = normaliza(base)
    s = normaliza(consulta) @ b.T
    if espelho:
        s = np.maximum(s, normaliza(consulta.flip(3)) @ b.T)
    return s.argmax(axis=1), s.max(axis=1)
