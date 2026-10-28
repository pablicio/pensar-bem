"""Vigiar o modelo em produção: a entrada muda antes."""
import numpy as np

PISO = 1e-4           # evita log de zero numa faixa vazia


def psi(referencia, nova, faixas=10):
    """O índice de estabilidade entre duas amostras."""
    passos = np.linspace(0, 1, faixas + 1)
    cortes = np.quantile(referencia, passos)
    cortes = np.unique(cortes)
    cortes[0], cortes[-1] = -np.inf, np.inf
    a = np.histogram(referencia, cortes)[0] / len(referencia)
    b = np.histogram(nova, cortes)[0] / len(nova)
    a, b = np.maximum(a, PISO), np.maximum(b, PISO)
    return float(((b - a) * np.log(b / a)).sum())


def psi_categorias(referencia, nova):
    """O mesmo índice, com uma faixa por categoria."""
    a = referencia.value_counts(normalize=True)
    b = nova.value_counts(normalize=True)
    a, b = a.align(b, fill_value=0)
    a, b = np.maximum(a, PISO), np.maximum(b, PISO)
    return float(((b - a) * np.log(b / a)).sum())


def estado(valor):
    if valor >= 0.25:
        return "alerta"
    return "atenção" if valor >= 0.10 else "estável"
