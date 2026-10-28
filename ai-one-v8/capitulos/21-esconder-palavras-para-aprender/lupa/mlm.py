"""O objetivo mascarado do BERT: esconder 15% e adivinhar."""
import torch


def especiais(V):
    """Três números depois do vocabulário."""
    return {"[MASK]": V, "[CLS]": V + 1, "[PAD]": V + 2}


def mascara(x, V, gerador=None, p=0.15):
    """A entrada corrompida e os alvos (-100: ignorar).

    Dos tokens escolhidos, 80% viram [MASK], 10% um token
    sorteado e 10% ficam como estão."""
    sorteio = torch.rand(x.shape, generator=gerador)
    escolhidos = sorteio < p
    alvo = torch.where(escolhidos, x, torch.full_like(x, -100))
    entrada = x.clone()
    u = torch.rand(x.shape, generator=gerador)
    entrada[escolhidos & (u < 0.8)] = especiais(V)["[MASK]"]
    troca = escolhidos & (u >= 0.8) & (u < 0.9)
    aleatorios = torch.randint(0, V, x.shape,
                               generator=gerador)
    entrada[troca] = aleatorios[troca]
    return entrada, alvo
