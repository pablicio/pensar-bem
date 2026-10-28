"""O scanner do inverno: cada cartão, quando for pedido."""
import numpy as np

from dados.formulario import cartao, estilo

GABARITO = [17, 714, 1, 280, 71, 365, 8, 117, 47, 900]
CARTOES = 24_600
VALENTINA = 1_877                   # a posição dela na pilha


def respostas(sorteio):
    r = []
    for certa in GABARITO:
        u = sorteio.random()
        if u < 0.06:
            r.append(None)          # deixou em branco
        elif u < 0.50:
            r.append(certa)
        else:
            r.append(int(sorteio.integers(0, 1000)))
    return r


def cartao_do_inverno(i):
    """O cartão i da pilha: inscrição, folha, respostas."""
    sorteio = np.random.default_rng([2027, i])
    e, r = estilo(sorteio), respostas(sorteio)
    if i == VALENTINA:              # estudou desde o verão
        e.update(sete_cortado=True, um_serifa=True,
                 zeros_a_esquerda=True)
        r = GABARITO[:9] + [90]
    folha = cartao(r, e, sorteio)
    return 60_000 + i, folha, r, e["zeros_a_esquerda"]
