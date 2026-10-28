"""O mundo da Dendê: datas, regiões, negócios e o sorteio."""
from datetime import date, timedelta
from pathlib import Path

import numpy as np

BRUTOS = Path("dados/brutos")
INICIO = date(2022, 1, 3)       # o primeiro da série
EXTRATO = date(2027, 3, 12)     # a extração que o Ícaro recebe
FIM = date(2027, 6, 30)         # a revisão do covenant
TAXA = 0.045                    # juros ao mês
rng = np.random.default_rng(2027)

# empréstimos concedidos por ano (2027: até o extrato)
POR_ANO = {2022: 2400, 2023: 3000, 2024: 3600, 2025: 7200,
           2026: 9600, 2027: 2400}

# região: peso, renda relativa, risco, prefixos de fixo
REGIOES = {
    "Centro": (0.12, 1.15, -0.20, ["3321", "3322", "3326"]),
    "Liberdade": (0.13, 0.90, 0.05, ["3241", "3242"]),
    "Subúrbio Ferroviário": (0.16, 0.80, 0.25,
                             ["3398", "3399", "3397"]),
    "Cajazeiras": (0.14, 0.85, 0.10, ["3394", "3393"]),
    "Itapuã": (0.12, 0.95, 0.00, ["3375", "3374"]),
    "Pituba e Rio Vermelho": (0.10, 1.30, -0.25,
                              ["3358", "3359"]),
    "Cabula": (0.11, 0.95, 0.00, ["3387", "3386"]),
    "Lauro de Freitas": (0.12, 1.05, -0.05, ["3379", "3378"]),
}

# negócio: peso, faturamento mediano (R$/mês), risco
NEGOCIOS = {
    "costura": (0.11, 3200, -0.25),
    "barbearia e salão": (0.13, 4200, -0.10),
    "food truck e lanches": (0.11, 6500, 0.10),
    "vendedor de praia": (0.09, 2800, 0.20),
    "técnico de celular": (0.08, 5200, -0.05),
    "mercearia": (0.12, 7800, -0.15),
    "artesanato": (0.08, 2200, 0.05),
    "ambulante de festas": (0.04, 3000, 0.45),
    "oficina": (0.09, 6800, -0.05),
    "manicure e estética": (0.09, 2600, 0.00),
    "roupas e acessórios": (0.06, 5400, 0.10),
}

CANAIS = ["rua", "feira", "loja", "online", "em casa"]
AGENTES = ["Dandara", "Rosilene", "Marcelo", "Joelma",
           "Tiago", "Cristiane"]
PRODUTOS = ["Capital de giro", "MEI Mais"]


def dia(n):
    return INICIO + timedelta(days=int(n))


def sorteia(opcoes, pesos, n):
    p = np.array(pesos, dtype=float)
    return rng.choice(opcoes, size=n, p=p / p.sum())


def parcela(valor, n):
    """A parcela fixa (tabela Price) de um empréstimo."""
    return valor * TAXA / (1 - (1 + TAXA) ** -n)


def gravar(tabela, nome):
    BRUTOS.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(BRUTOS / nome, index=False,
                  lineterminator="\n")
