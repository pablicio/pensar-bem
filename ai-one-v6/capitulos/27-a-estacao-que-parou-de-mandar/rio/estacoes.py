"""As estações rio acima: as colunas de cada uma e o sensor
travado."""
ESTACOES = ["rio_do_sul", "apiuna"]
TRAVADA = 15        # leituras iguais seguidas: o sensor parou


def colunas_de(estacao):
    """O nível, a subida e a chuva de uma estação."""
    return [estacao, f"sobe_{estacao}", f"chuva_{estacao}"]


def travada(serie):
    """As últimas TRAVADA leituras são todas iguais."""
    fim = serie.iloc[-TRAVADA:]
    return bool(fim.notna().all() and fim.nunique() == 1)
