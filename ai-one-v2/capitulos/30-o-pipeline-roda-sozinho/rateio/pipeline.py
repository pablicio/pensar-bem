"""O rateio de um mês, do dado bruto ao arquivo da GED."""
import logging
from pathlib import Path

import pandas as pd

from rateio import manifesto
from rateio.calculo import sobra
from rateio.dicionario import FONTES
from rateio.geracao import geracao_diaria
from rateio.leitura import (BRUTOS, ler_abadiania,
                            ler_cadastro, ler_corumba)
from rateio.limpeza import cpf_normalizado

log = logging.getLogger("rateio")


class DadosInesperados(Exception):
    """Os dados brutos não estão como o pipeline espera."""


def confere_brutos(config):
    """Para tudo se um arquivo bruto mudou ou sumiu."""
    antes = manifesto.ler(config["manifesto"])
    agora = manifesto.gerar(config["brutos"])
    mudou = manifesto.comparar(antes, agora)
    for nome in mudou["alterados"]:
        log.error("alterado: %s", nome)
    for nome in mudou["faltando"]:
        log.error("faltando: %s", nome)
    for nome in mudou["novos"]:
        log.warning("fora do manifesto: %s", nome)
    if mudou["alterados"] or mudou["faltando"]:
        raise DadosInesperados("brutos fora do manifesto")
    log.info("brutos conferidos: %d arquivos", len(agora))


def confere_colunas(mes):
    """Para tudo se uma fonte mudou de colunas."""
    lidas = {"corumba": ler_corumba(mes),
             "abadiania": ler_abadiania(mes),
             "cadastro": ler_cadastro()}
    for fonte, tabela in lidas.items():
        if list(tabela.columns) != FONTES[fonte]["colunas"]:
            raise DadosInesperados(f"{fonte} mudou de colunas")
    log.info("colunas conferidas com o dicionário de dados")


def calcula(mes, tarifa):
    """A geração de cada usina e o crédito de cada um."""
    leituras = geracao_diaria(mes)
    geracao = leituras.groupby("usina")["kwh"].sum().round(3)
    for usina, kwh in geracao.items():
        log.info("geração %-17s %12.3f kWh", usina, kwh)
    cad = ler_cadastro()
    ativos = cad[cad["Situação"] == "Ativo"]
    kwh = (ativos["Usina"].map(geracao)
           * ativos["Cota (%)"] / 100).round(2)
    envio = pd.DataFrame({
        "CPF": cpf_normalizado(ativos["CPF"]),
        "Nome": ativos["Nome"], "Usina": ativos["Usina"],
        "kWh": kwh, "Valor": (kwh * tarifa).round(2)})
    return geracao, envio


def rodar(mes, config):
    """O rateio do mês, gravado em <saida>/<mes>/."""
    confere_brutos(config)
    confere_colunas(mes)
    geracao, envio = calcula(mes, config["tarifa"])
    for usina, kwh in geracao.items():
        reais = envio.loc[envio["Usina"] == usina, "Valor"]
        log.info("sobra para a sede, %s: R$ %.2f", usina,
                 sobra(kwh, reais, config["tarifa"]))
    total = envio["Valor"].sum()
    log.info("%d cooperados, R$ %s", len(envio),
             f"{total:,.2f}")

    pasta = Path(config["saida"]) / mes
    arquivo = pasta / f"envio_ged_{mes}.csv"
    para_ged = envio.drop(columns="Usina")
    para_ged.to_csv(arquivo, sep=";", decimal=",", index=False)
    entradas = [BRUTOS / "cadastro_cooperados.xlsx",
                *sorted(BRUTOS.glob(f"inversores/*/*{mes}*"))]
    origem = manifesto.registrar_origem(arquivo, entradas,
                                        "python -m rateio")
    log.info("gravado %s", arquivo.as_posix())
    log.info("sha256 do envio: %s...", origem["sha256"][:16])
