"""Ler ou mandar para a revisão: a regra do custo."""
TEMPERATURA = 1.315   # a do capítulo 22
REVISAO = 0.16        # reais por caixa: R$ 118 mil / 738 mil


def limiar(custo_erro, custo_revisao=REVISAO):
    """Abaixo desta confiança, revisar custa menos que ler."""
    return 1 - custo_revisao / custo_erro


def decide(logitos, lim):
    """A leitura, a confiança e se a rede pode ler sozinha."""
    p = (logitos / TEMPERATURA).softmax(dim=1)
    confianca, leitura = p.max(dim=1)
    return leitura, confianca, confianca >= lim
