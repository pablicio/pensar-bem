"""Depois do extrato: os pedidos até junho e o fechamento."""
from datetime import date, timedelta

import numpy as np
import pandas as pd

from carteira import emprestimo, novo_cliente, risco
from cobranca import desfecho, situacao
from gerar_carteira import escolhe_cliente, gerar, registra
from mundo import NEGOCIOS, gravar, rng

INICIO = date(2027, 3, 15)        # a segunda depois do extrato
FIM = date(2027, 6, 11)           # o último pedido da série
OLHAR = date(2027, 6, 14)         # o Ícaro olha a cobrança
FECHAMENTO = date(2027, 6, 30)    # o covenant é medido
POR_DIA = 45
FESTA = date(2027, 5, 10)         # chegam os ambulantes
EXTRA_FESTA = 18                  # pedidos a mais por dia


def ambulante(n, quando):
    """Um cliente novo que vende na festa: negócio recente."""
    c = novo_cliente(n, quando)
    c["tipo"] = "ambulante de festas"
    mediano = NEGOCIOS["ambulante de festas"][1]
    c["faturamento"] = float(mediano * rng.lognormal(0, 0.35))
    c["inicio_negocio"] = quando - timedelta(
        days=int(rng.gamma(1.5, 60)))
    return c


def um_pedido(clientes, dia, n, festa):
    if festa:
        c = ambulante(len(clientes) + 1, dia)
        clientes.append(c)
    else:
        c = escolhe_cliente(clientes, dia, len(clientes) + 1)
    c["atrasos"] = sum(1 for d in c.get("atrasos_em", [])
                       if d < dia)
    e = emprestimo(c, dia, n)
    if festa:
        e["canal"] = str(rng.choice(["feira", "rua"]))
    f = desfecho(e, risco(c, e, dia))
    registra(c, e, f)
    return e, f


def producao():
    clientes, antigos, fins = gerar()   # o mundo do extrato
    # daqui em diante, outro sorteio: o extrato não muda
    rng.bit_generator.state = (
        np.random.default_rng(2028).bit_generator.state)
    n = len(antigos)
    novos, novos_fins = [], []
    dia = INICIO
    while dia <= FIM:
        if dia.weekday() < 5:
            extra = EXTRA_FESTA if dia >= FESTA else 0
            for k in range(POR_DIA + extra):
                n += 1
                festa = k >= POR_DIA
                e, f = um_pedido(clientes, dia, n, festa)
                novos.append(e)
                novos_fins.append(f)
        dia += timedelta(days=1)
    olhar = [situacao(e, f, OLHAR)
             for e, f in zip(novos, novos_fins)]
    todos = zip(antigos + novos, fins + novos_fins)
    fecha = [situacao(e, f, FECHAMENTO) for e, f in todos]
    return (pd.DataFrame(novos), pd.DataFrame(olhar),
            pd.DataFrame(fecha))


if __name__ == "__main__":
    pedidos, olhar, fecha = producao()
    colunas = ["pedido_id", "cliente_id", "data_concessao",
               "produto", "valor", "parcelas", "finalidade",
               "tipo_negocio", "canal", "idade",
               "tempo_negocio_meses", "cliente_desde_meses",
               "emprestimos_anteriores", "atrasos_anteriores",
               "faturamento_declarado", "telefone_referencia",
               "agente"]
    gravar(pedidos[colunas], "producao_pedidos.csv")
    gravar(olhar, "producao_cobranca.csv")
    gravar(fecha, "fechamento_cobranca.csv")
    print(f"{len(pedidos):,} pedidos de {INICIO} a {FIM}")
