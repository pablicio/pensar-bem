"""Um vetor por texto e a perda que junta os que combinam."""
import torch
import torch.nn.functional as F

from .ajuste import tensores


def vetores(bert, textos, tok, T=128, B=128):
    """A média dos estados, normalizada: cosseno = produto."""
    ids, vazio = tensores(textos, tok, T)
    saida = []
    for i in range(0, len(ids), B):
        h = bert(ids[i:i + B], vazio[i:i + B])
        cheio = (~vazio[i:i + B]).unsqueeze(-1).float()
        media = (h * cheio).sum(1) / cheio.sum(1)
        saida.append(F.normalize(media, dim=-1))
    return torch.cat(saida)


def infonce(q, d, tau=0.1):
    """q[i] combina com d[i]; os outros d são negativos."""
    notas = q @ d.T / tau                 # (B, B)
    certo = torch.arange(len(q))
    return F.cross_entropy(notas, certo)
