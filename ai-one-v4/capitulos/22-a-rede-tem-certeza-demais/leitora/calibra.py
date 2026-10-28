"""Calibração: o erro de calibração e a temperatura."""
import torch
import torch.nn.functional as F


def por_faixa(prob, rotulos, faixas=10):
    """Confiança média e acerto em cada faixa de confiança."""
    confianca, previsto = prob.max(dim=1)
    certo = (previsto == rotulos).float()
    limites = torch.linspace(0, 1, faixas + 1)
    linhas = []
    for a, b in zip(limites[:-1], limites[1:]):
        dentro = (confianca > a) & (confianca <= b)
        if dentro.any():
            linhas.append((a.item(), b.item(),
                           int(dentro.sum()),
                           confianca[dentro].mean().item(),
                           certo[dentro].mean().item()))
    return linhas


def erro_de_calibracao(prob, rotulos, faixas=10):
    """ECE: a distância média entre confiança e acerto."""
    n = len(rotulos)
    return sum(k / n * abs(conf - acerto)
               for _, _, k, conf, acerto
               in por_faixa(prob, rotulos, faixas))


def temperatura(logitos, rotulos, passos=200):
    """A temperatura que minimiza a entropia cruzada."""
    log_t = torch.zeros(1, requires_grad=True)
    otimizador = torch.optim.Adam([log_t], lr=0.05)
    for _ in range(passos):
        otimizador.zero_grad()
        perda = F.cross_entropy(logitos / log_t.exp(), rotulos)
        perda.backward()
        otimizador.step()
    return log_t.exp().item()
