"""O nível da cidade, limpo, na escala da régua nova."""
import pandas as pd

REGUA_NOVA = pd.Timestamp("1996-07-01")
DEGRAU = 0.37        # o levantamento da régua nova, em metros


def ler(nome):
    """Uma tabela de dados/brutos com o índice de datas."""
    return pd.read_csv(f"dados/brutos/{nome}.csv",
                       parse_dates=["data_hora"],
                       index_col="data_hora")


def digitacao(leitura):
    """Leituras com um zero a mais: dez vezes a vizinhança."""
    vizinhas = leitura.rolling(5, center=True,
                               min_periods=3).median()
    return (leitura / vizinhas).between(8, 12)


def preenche(serie, maximo):
    """Interpola só as lacunas de até `maximo` horas."""
    falta = serie.isna()
    bloco = (falta != falta.shift()).cumsum()
    tamanho = falta.groupby(bloco).transform("sum")
    cheia = serie.interpolate(limit_area="inside")
    return cheia.where(~falta | (tamanho <= maximo))


def nivel_cidade(maximo=3):
    """O nível da cidade, em metros, de hora em hora."""
    leitura = ler("cadernos")["leitura_cm"].astype(float)
    erro = digitacao(leitura)
    leitura[erro] = leitura[erro] / 10
    nivel = leitura / 100
    nivel[nivel.index < REGUA_NOVA] += DEGRAU
    return preenche(nivel.asfreq("h"), maximo)
