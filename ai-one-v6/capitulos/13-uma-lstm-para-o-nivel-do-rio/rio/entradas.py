"""As séries do rio numa tabela, e a escala do treino."""
import pandas as pd

from rio.avalia import parte
from rio.serie import ler, nivel_cidade, preenche

NIVEIS = ["cidade", "rio_do_sul", "apiuna"]
CHUVAS = ["taio", "ituporanga", "rio_do_sul", "apiuna"]


def tabela():
    """Uma linha por hora: os três níveis (m), as quatro chuvas
    (mm) e quantos pluviômetros estão sem dado naquela hora.

    Regra provisória para as lacunas (o capítulo 27 volta a
    ela): nível de estação, interpolado até 24 horas; chuva que
    falta vira zero, e a coluna `faltam` avisa."""
    tele = ler("telemetria")
    tab = pd.DataFrame({"cidade": nivel_cidade()})
    for nome in NIVEIS[1:]:
        tab[nome] = preenche(tele[f"nivel_{nome}"] / 100, 24)
    chuvas = tele[CHUVAS].add_prefix("chuva_")
    tab["faltam"] = chuvas.isna().sum(axis=1)
    return tab.join(chuvas.fillna(0.0))


class Escala:
    """Média e desvio de cada coluna, medidos só no treino."""

    def __init__(self, tab):
        treino = parte(tab, "treino")
        self.media = treino.mean()
        self.desvio = treino.std()

    def aplica(self, tab):
        return (tab - self.media) / self.desvio


def com_subidas(tab):
    """Acrescenta a subida de cada nível na última hora."""
    nova = tab.copy()
    for nome in NIVEIS:
        nova[f"sobe_{nome}"] = tab[nome].diff()
    return nova
