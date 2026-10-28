"""O plantão: a cada hora, ler a telemetria, prever, avisar."""
import pandas as pd
import torch

from rio.alerta import maximo_previsto
from rio.avalia import parte
from rio.entradas import CHUVAS, NIVEIS, com_subidas
from rio.estacoes import ESTACOES, colunas_de, travada
from rio.quantis import preve_quantis
from rio.reserva import chuva_24h
from rio.serie import preenche

COTA = 5.5


def para_tabela(tele):
    """A telemetria nova (em cm, com o nível da cidade) nas
    colunas do treino, com as lacunas do capítulo 12."""
    tab = pd.DataFrame({"cidade": tele["nivel_cidade"] / 100})
    for nome in NIVEIS[1:]:
        tab[nome] = preenche(tele[f"nivel_{nome}"] / 100, 24)
    chuvas = tele[CHUVAS].add_prefix("chuva_")
    tab["faltam"] = chuvas.isna().sum(axis=1)
    return com_subidas(tab.join(chuvas.fillna(0.0)))


def aviso(teto):
    return (f"DEFESA CIVIL: o rio pode passar de {COTA:.1f} m"
            f" nas proximas 12 h (ate {teto:.1f} m)."
            " Prepare-se para sair e acompanhe os avisos.")


class Plantao:
    def __init__(self, modelo, escala, historico,
                 reservas=None):
        """`reservas`: estação -> (modelo, escala) treinados
        sem as colunas daquela estação."""
        self.modelo, self.escala = modelo, escala
        self.reservas = reservas or {}
        treino = parte(historico, "treino")
        self.teto_nivel = treino["cidade"].max()
        self.teto_chuva = chuva_24h(treino).max()
        self.alarme = False

    def fora_do_ar(self, tab):
        """Estações com buraco na janela ou sensor travado."""
        janela = tab.iloc[-72:]
        return [e for e in ESTACOES if janela[e].isna().any()
                or travada(janela[e])]

    def hora(self, tele):
        """Uma rodada, com as horas recebidas até agora."""
        tab = para_tabela(tele.iloc[-100:])
        nivel = float(tab["cidade"].iloc[-1])
        falta = self.fora_do_ar(tab)
        linha = {"hora": tab.index[-1], "nivel": nivel,
                 "mediana": None, "teto": None,
                 "largura": None, "alarme": self.alarme,
                 "chamada": False, "fora": ",".join(falta),
                 "nota": ""}
        modelo, escala = self.modelo, self.escala
        entrada = tab
        if len(falta) == 1 and falta[0] in self.reservas:
            modelo, escala = self.reservas[falta[0]]
            entrada = tab.drop(columns=colunas_de(*falta))
        elif falta:
            linha["nota"] = "sem previsão: " + linha["fora"]
            return linha
        janela = escala.aplica(entrada).iloc[-72:]
        x = torch.tensor(janela.to_numpy()[None],
                         dtype=torch.float32)
        q = preve_quantis(modelo, x)            # (1, 12, 3)
        mediana = maximo_previsto(nivel, q, 1)[0]
        teto = maximo_previsto(nivel, q, 2)[0]
        linha["mediana"] = float(mediana)
        linha["teto"] = float(teto)
        linha["largura"] = float(q[0, -1, 2] - q[0, -1, 0])
        linha["alarme"] = linha["teto"] >= COTA
        fora = (nivel > self.teto_nivel
                or bool((chuva_24h(tab).iloc[-1]
                         > self.teto_chuva).any()))
        subindo = nivel - tab["cidade"].iloc[-4] > 0.3
        linha["chamada"] = fora and subindo
        if linha["alarme"] and not self.alarme:
            linha["nota"] = aviso(linha["teto"])
        elif self.alarme and not linha["alarme"]:
            linha["nota"] = "fim do alarme"
        self.alarme = linha["alarme"]
        return linha
