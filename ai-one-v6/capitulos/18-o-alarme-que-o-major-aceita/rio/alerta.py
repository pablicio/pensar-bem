"""A política de alarme e o custo das decisões, em milhões."""
import numpy as np

FALSO = 0.38       # um alarme falso: a noite do ginásio
PERDIDA = 15.0     # uma cheia sem aviso (uma estimativa)
PRAZO = 6          # horas para tirar um bairro


def custo(antecedencias, cheias, falsos):
    """Cheia avisada com menos de PRAZO horas custa meia cheia
    perdida: dá tempo de avisar, não de tirar todo mundo."""
    tarde = sum(a < PRAZO for a in antecedencias)
    perdidas = cheias - len(antecedencias)
    return falsos * FALSO + (perdidas + tarde / 2) * PERDIDA


def limiar():
    """A chance de cheia acima da qual vale tocar o alarme."""
    return FALSO / (FALSO + PERDIDA)


def maximo_previsto(agora, quantis, k):
    """O maior nível previsto para as próximas horas, no
    quantil de índice k."""
    return agora + np.max(quantis[:, :, k], axis=1)
