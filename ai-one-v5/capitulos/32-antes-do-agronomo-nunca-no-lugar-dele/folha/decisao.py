"""Probabilidades honestas: dobras, calibração, temperatura."""
import torch

from folha.conjunto import parte, tabela
from folha.emprestada import treina_cabeca


def notas_fora_da_dobra(x, y):
    """Notas do treino, cada fazenda julgada por uma cabeça que
    não a viu (capítulos 18 e 20)."""
    linhas = [f for f in tabela()
              if parte(f["fazenda"]) == "treino"]
    fazendas = sorted({f["fazenda"] for f in linhas})
    dobra = torch.tensor([fazendas.index(f["fazenda"]) % 5
                          for f in linhas])
    notas = torch.zeros(len(y), 6)
    for k in range(5):
        cabeca = treina_cabeca(x[dobra != k], y[dobra != k])
        with torch.no_grad():
            notas[dobra == k] = cabeca(x[dobra == k])
    return notas


def ece(prob, y, faixas=10):
    """Erro de calibração esperado: a média, pesada pelo número
    de fotos, de |acerto − confiança| em cada faixa."""
    conf, prevista = prob.max(dim=1)
    certo = (prevista == y).float()
    total = 0.0
    for i in range(faixas):
        baixo, alto = i / faixas, (i + 1) / faixas
        dentro = (conf > baixo) & (conf <= alto)
        if dentro.any():
            lacuna = certo[dentro].mean() - conf[dentro].mean()
            total += dentro.float().mean() * lacuna.abs()
    return float(total)


def temperatura(notas, y):
    """A temperatura T que minimiza a entropia cruzada de
    softmax(notas / T) (Guo et al., 2017)."""
    log_t = torch.zeros(1, requires_grad=True)
    otimizador = torch.optim.LBFGS([log_t], max_iter=100)

    def passo():
        otimizador.zero_grad()
        perda = torch.nn.functional.cross_entropy(
            notas / log_t.exp(), y)
        perda.backward()
        return perda

    otimizador.step(passo)
    return log_t.exp().item()
