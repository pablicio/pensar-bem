"""Maneiras de escolher o próximo token pelos logits."""
import torch


def gulosa(logits):
    return logits.argmax(-1, keepdim=True)


def amostra(temperatura=1.0, k=None, p=None, gerador=None):
    """Temperatura, depois top-k e top-p, depois sorteio."""
    def escolhe(logits):
        z = logits / temperatura
        if k is not None:                 # só os k maiores
            corte = z.topk(k, dim=-1).values[..., -1:]
            z = z.masked_fill(z < corte, float("-inf"))
        if p is not None:                 # o núcleo, massa p
            z_ord, ordem = z.sort(-1, descending=True)
            acum = z_ord.softmax(-1).cumsum(-1)
            fora = acum - z_ord.softmax(-1) >= p
            z_ord = z_ord.masked_fill(fora, float("-inf"))
            z = z.scatter(-1, ordem, z_ord)
        probs = z.softmax(-1)
        return torch.multinomial(probs, 1, generator=gerador)
    return escolhe
