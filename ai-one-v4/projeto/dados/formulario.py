"""O cartão-resposta: dez questões, três caixas cada."""
import numpy as np
from PIL import Image

from dados.desenho import LADO, desenha
from dados.tracos import TRACOS

CAIXA, PASSO = 40, 48       # lado da caixa e espaçamento
MARGEM_X, MARGEM_Y = 20, 60
LARGURA = MARGEM_X * 2 + 2 * PASSO + CAIXA
ALTURA = MARGEM_Y + 9 * PASSO + CAIXA + 20


def posicao(questao, caixa):
    """O canto de cima, à esquerda, de uma caixa do cartão."""
    return MARGEM_X + caixa * PASSO, MARGEM_Y + questao * PASSO


def estilo(sorteio):
    """O jeito de escrever de uma pessoa."""
    return {"sete_cortado": sorteio.random() < 0.55,
            "um_serifa": sorteio.random() < 0.5,
            "quatro_aberto": sorteio.random() < 0.4,
            "espessura": sorteio.uniform(9, 16),
            "zeros_a_esquerda": sorteio.random() < 0.5}


def variante(digito, e):
    v = TRACOS[digito]
    if digito == 7:
        return v[1] if e["sete_cortado"] else v[0]
    if digito == 1:
        return v[1] if e["um_serifa"] else v[0]
    if digito == 4:
        return v[1] if e["quatro_aberto"] else v[0]
    return v[0]


def caixas_da_resposta(resposta, e):
    """Os três dígitos escritos; None é caixa em branco."""
    if resposta is None:
        return [None, None, None]
    texto = f"{resposta:03d}"
    if not e["zeros_a_esquerda"]:
        texto = f"{resposta:>3d}"
    return [None if c == " " else int(c) for c in texto]


def cartao(respostas, e, sorteio):
    """A folha escaneada: papel, caixas, tinta e ruído."""
    folha = np.full((ALTURA, LARGURA), 235.0)
    for q, resposta in enumerate(respostas):
        for k, d in enumerate(caixas_da_resposta(resposta, e)):
            x, y = posicao(q, k)
            folha[y:y + CAIXA, [x, x + CAIXA - 1]] = 150
            folha[[y, y + CAIXA - 1], x:x + CAIXA] = 150
            if d is None:
                continue
            esp = e["espessura"] * sorteio.uniform(0.9, 1.1)
            img = desenha(variante(d, e), sorteio, esp)
            lado = CAIXA - 6
            img = img.resize((lado, lado), Image.LANCZOS)
            tinta = np.asarray(img, dtype=float) / 255
            dx, dy = sorteio.integers(1, 6, size=2)
            reg = folha[y + dy:y + dy + CAIXA - 6,
                        x + dx:x + dx + CAIXA - 6]
            np.minimum(reg, 235 - 195 * tinta, out=reg)
    folha += sorteio.normal(0, 6, folha.shape)    # o scanner
    return np.clip(folha, 0, 255).astype(np.uint8)
