"""Clientes e empréstimos, em ordem de data, com o risco."""
from datetime import timedelta

import numpy as np

from mundo import (AGENTES, CANAIS, EXTRATO, INICIO, NEGOCIOS,
                   POR_ANO, REGIOES, parcela, rng, sorteia)
from textos import PESOS, escreve

NOMES = ["Ana", "Maria", "Jorge", "Antônio", "Rita", "Carla",
         "Luana", "Edson", "Valdir", "Jaqueline", "Joana",
         "Raimundo", "Cleide", "Gilmar", "Iara", "Rose",
         "Josué", "Marli", "Danilo", "Tânia", "Railda",
         "Ubiratã", "Neide", "Cosme"]
SOBRENOMES = ["Santos", "Souza", "Silva", "Conceição", "Jesus",
              "Oliveira", "Nascimento", "Bonfim", "Barbosa",
              "Reis", "Pereira", "Lima", "Carvalho", "Brito"]
GOLPE_FONE = "(71) 98877-1203"


def datas_dos_emprestimos():
    """Um dia útil para cada empréstimo, ano a ano."""
    dias = []
    for ano, n in POR_ANO.items():
        fim = EXTRATO if ano == 2027 else INICIO.replace(
            year=ano, month=12, day=31)
        ini = max(INICIO, INICIO.replace(year=ano, day=1))
        uteis = [ini + timedelta(d)
                 for d in range((fim - ini).days + 1)]
        uteis = [d for d in uteis if d.weekday() < 5]
        dias += list(rng.choice(uteis, size=n))
    return sorted(dias)


def telefone(regiao):
    if rng.random() < 0.6:
        prefixo = rng.choice(REGIOES[regiao][3])
        return f"(71) {prefixo}-{rng.integers(1000, 9999)}"
    return (f"(71) 9{rng.integers(8100, 9999)}-"
            f"{rng.integers(1000, 9999)}")


def novo_cliente(n, quando):
    pesos = [r[0] for r in REGIOES.values()]
    regiao = str(sorteia(list(REGIOES), pesos, 1)[0])
    pesos = [g[0] for g in NEGOCIOS.values()]
    tipo = str(sorteia(list(NEGOCIOS), pesos, 1)[0])
    if quando.month in (5, 6) and rng.random() < 0.15:
        tipo = "ambulante de festas"     # chega o São João
    renda = REGIOES[regiao][1]
    mediano = NEGOCIOS[tipo][1] * renda
    idade = int(rng.integers(20, 68))
    medo = rng.random() < (0.45 if idade >= 45 else 0.18)
    nome = rng.choice(NOMES)
    sobrenome = rng.choice(SOBRENOMES)
    return {
        "cliente_id": f"C{n:05d}",
        "nome": f"{nome} {sobrenome}",
        "regiao": regiao, "tipo": tipo,
        "idade0": idade, "desde": quando,
        "inicio_negocio": quando - timedelta(
            days=int(rng.gamma(2.0, 400))),
        "faturamento": float(mediano * rng.lognormal(0, 0.35)),
        "declara": float(rng.uniform(0.40, 0.62) if medo
                         else rng.uniform(0.85, 1.10)),
        "mei": bool(rng.random() < 0.35),
        "telefone": telefone(regiao),
        "agente": AGENTES[list(REGIOES).index(regiao) % 6],
        "emprestimos": 0, "atrasos": 0,
        "livre_em": quando, "bloqueado": False,
    }


def risco(c, e, quando):
    """A probabilidade real de chegar a 90 dias em atraso."""
    z = -1.80
    z += 8.0 * (e["comprometimento_real"] - 0.12)
    z += 1.4 * c["atrasos"]
    z -= 0.85 * np.log1p(e["tempo_negocio_meses"] / 12)
    z -= 0.30 * min(c["emprestimos"], 3)
    z += NEGOCIOS[c["tipo"]][2] + REGIOES[c["regiao"]][2]
    z += 1.0 * (e["categoria"] == "pagar dívida")
    z += 0.70 * (e["idade"] < 25) + 0.25 * (e["idade"] > 60)
    z += {"online": 0.60, "em casa": -0.20}.get(e["canal"], 0)
    novo = c["emprestimos"] == 0
    z += 0.60 * (novo and quando.year in (2025, 2026))
    z -= 1.3 * (e["produto"] == "MEI Mais")
    festa = c["tipo"] == "ambulante de festas"
    z += 0.8 * (festa and quando.month in (5, 6))
    z += rng.normal(0, 0.25)
    return 1 / (1 + np.exp(-z))


def emprestimo(c, quando, n):
    meses_negocio = (quando - c["inicio_negocio"]).days // 30
    fat = c["faturamento"] * rng.lognormal(0, 0.08)
    declarado = round(fat * c["declara"], -1)
    if c["emprestimos"] == 0:
        valor = rng.uniform(500, 3500)
    else:
        valor = rng.uniform(1500, 5000)
        valor *= 1 + 0.2 * c["emprestimos"]
    valor = float(min(8000, max(300, round(valor, -1))))
    parcelas = int(rng.choice([6, 9, 12, 15, 18],
                              p=[.2, .2, .3, .15, .15]))
    linha_mei = quando >= INICIO.replace(year=2026)
    mei_mais = c["mei"] and linha_mei and rng.random() < 0.5
    categoria = str(sorteia(list(PESOS), list(PESOS.values()),
                            1)[0])
    finalidade = escreve(categoria)
    canal = str(rng.choice(CANAIS))
    p = parcela(valor, parcelas)
    anos = (quando - c["desde"]).days // 365
    meses_cliente = (quando - c["desde"]).days // 30
    return {
        "pedido_id": f"P{n:05d}",
        "cliente_id": c["cliente_id"],
        "data_concessao": quando,
        "produto": ("MEI Mais" if mei_mais
                    else "Capital de giro"),
        "valor": valor, "parcelas": parcelas,
        "finalidade": finalidade, "categoria": categoria,
        "tipo_negocio": c["tipo"], "regiao": c["regiao"],
        "canal": canal,
        "idade": c["idade0"] + anos,
        "tempo_negocio_meses": int(meses_negocio),
        "cliente_desde_meses": meses_cliente,
        "emprestimos_anteriores": c["emprestimos"],
        "atrasos_anteriores": c["atrasos"],
        "faturamento_declarado": float(declarado),
        "faturamento_real": round(fat, 2),
        "comprometimento_real": p / fat,
        "telefone_referencia": c["telefone"],
        "mei": c["mei"], "agente": c["agente"],
    }
