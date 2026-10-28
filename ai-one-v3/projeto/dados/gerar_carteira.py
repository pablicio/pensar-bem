"""Gera a carteira sintética da Dendê Crédito em dados/brutos.

    python dados/gerar_carteira.py
"""
from datetime import date, timedelta

import pandas as pd

from carteira import (GOLPE_FONE, datas_dos_emprestimos,
                      emprestimo, novo_cliente, risco)
from cobranca import desfecho, situacao
from mundo import EXTRATO, gravar, rng

REPETE = {2022: 0.25, 2023: 0.40, 2024: 0.50, 2025: 0.30,
          2026: 0.45, 2027: 0.50}
CIDA = [date(2022, 2, 14), date(2023, 1, 16),
        date(2023, 11, 20), date(2024, 10, 7),
        date(2025, 8, 11), date(2026, 7, 6), date(2027, 3, 8)]
GOLPE = [date(2027, 2, 8) + timedelta(days=d % 5)
         for d in range(9)]


def dona_cida():
    c = novo_cliente(0, date(2021, 3, 1))
    c.update({"cliente_id": "C00000",
              "nome": "Aparecida Santos", "regiao": "Itapuã",
              "tipo": "costura", "idade0": 53,
              "inicio_negocio": date(2019, 5, 1),
              "faturamento": 4200.0, "declara": 0.43,
              "mei": False, "telefone": "(71) 3375-2210",
              "agente": "Dandara"})
    return c


def golpista(n):
    c = novo_cliente(n, GOLPE[0])
    c.update({"tipo": "roupas e acessórios",
              "regiao": "Centro", "telefone": GOLPE_FONE,
              "agente": "Tiago", "faturamento": 9500.0,
              "declara": 1.0,
              "idade0": int(rng.integers(23, 32)),
              "inicio_negocio": GOLPE[0] - timedelta(900)})
    return c


def escolhe_cliente(clientes, quando, n):
    """Um cliente antigo que pode renovar, ou um novo."""
    if clientes and rng.random() < REPETE[quando.year]:
        for _ in range(25):
            c = clientes[int(rng.integers(len(clientes)))]
            if (not c["bloqueado"] and c["livre_em"] <= quando
                    and c["cliente_id"] != "C00000"):
                return c
    c = novo_cliente(n, quando)
    clientes.append(c)
    return c


def registra(c, e, f):
    """Atualiza o histórico do cliente depois da concessão."""
    c["emprestimos"] += 1
    meio = (e["parcelas"] + 1) // 2
    c["livre_em"] = e["data_concessao"] + timedelta(30 * meio)
    if f["para_em"] is not None:
        c["bloqueado"] = True
    if f["atraso_dias"] >= 30:
        c.setdefault("atrasos_em", []).append(f["atraso_em"])


def gerar():
    clientes, emprestimos, desfechos = [dona_cida()], [], []
    agenda = [(d, "comum") for d in datas_dos_emprestimos()]
    agenda += [(d, "cida") for d in CIDA]
    agenda += [(d, "golpe") for d in GOLPE]
    agenda.sort(key=lambda x: (x[0], x[1]))
    for n, (quando, quem) in enumerate(agenda, start=1):
        if quem == "cida":
            c = clientes[0]
        elif quem == "golpe":
            c = golpista(len(clientes) + 1)
            clientes.append(c)
        else:
            novo = len(clientes) + 1
            c = escolhe_cliente(clientes, quando, novo)
        c["atrasos"] = sum(1 for d in c.get("atrasos_em", [])
                           if d < quando)
        e = emprestimo(c, quando, n)
        if quem == "cida" and quando == CIDA[-1]:
            e.update({"valor": 6000.0, "parcelas": 12})
        if quem == "golpe":
            e.update({"valor": 8000.0, "parcelas": 18,
                      "canal": "online",
                      "categoria": "estoque",
                      "finalidade": "comprar mercadoria",
                      "faturamento_declarado": 9500.0})
        p = risco(c, e, quando)
        p = {"cida": 0.0, "golpe": 1.0}.get(quem, p)
        f = desfecho(e, p)
        if quem == "golpe":
            f["para_em"] = quando + timedelta(days=30)
        e["risco_real"] = p
        registra(c, e, f)
        emprestimos.append(e)
        desfechos.append(f)
    return clientes, emprestimos, desfechos


def exportar(clientes, emprestimos, desfechos, hoje):
    tab = pd.DataFrame(emprestimos)
    cad = pd.DataFrame(clientes).rename(
        columns={"tipo": "tipo_negocio",
                 "telefone": "telefone_referencia"})
    gravar(cad[["cliente_id", "nome", "regiao", "tipo_negocio",
                "telefone_referencia", "mei"]], "clientes.csv")
    colunas = ["pedido_id", "cliente_id", "data_concessao",
               "produto", "valor", "parcelas", "finalidade",
               "tipo_negocio", "canal", "idade",
               "tempo_negocio_meses", "cliente_desde_meses",
               "emprestimos_anteriores", "atrasos_anteriores",
               "faturamento_declarado", "telefone_referencia",
               "agente"]
    gravar(tab[colunas], "emprestimos.csv")
    situ = [situacao(e, f, hoje)
            for e, f in zip(emprestimos, desfechos)]
    gravar(pd.DataFrame(situ), "cobranca.csv")
    visitados = tab[tab["cliente_id"] != "C00000"].sample(
        n=2400, random_state=2027)
    fat = visitados["faturamento_real"].to_numpy()
    erro = rng.normal(1, 0.06, len(fat))
    gravar(pd.DataFrame({
        "pedido_id": visitados["pedido_id"].to_numpy(),
        "data_visita": visitados["data_concessao"].to_numpy(),
        "faturamento_verificado": (fat * erro).round(-1)}),
        "visitas.csv")
    rotulo = tab.sample(n=1500, random_state=7)
    gravar(rotulo[["pedido_id", "categoria"]].rename(
        columns={"categoria": "finalidade_categoria"}),
        "finalidades_rotuladas.csv")
    return tab


if __name__ == "__main__":
    clientes, emprestimos, desfechos = gerar()
    tab = exportar(clientes, emprestimos, desfechos, EXTRATO)
    print(f"{len(tab):,} empréstimos, "
          f"{tab['cliente_id'].nunique():,} clientes")
