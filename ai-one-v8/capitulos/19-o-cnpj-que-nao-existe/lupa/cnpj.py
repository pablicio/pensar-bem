"""O CNPJ e os seus dois dígitos verificadores."""
import re

from dados.nomes import dv_cnpj

FORMATO = re.compile(r"\d\d\.\d{3}\.\d{3}/\d{4}-\d\d")


def valido(cnpj):
    """Os dois últimos dígitos conferem com os doze antes?"""
    d = re.sub(r"\D", "", cnpj)
    return dv_cnpj(d[:12]) == [int(d[12]), int(d[13])]
