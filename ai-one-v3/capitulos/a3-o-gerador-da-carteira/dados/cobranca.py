"""Depois da concessão: pagar em dia, atrasar ou parar."""
from datetime import timedelta

from mundo import rng


def desfecho(e, p):
    """Sorteia, pelo risco p, como o empréstimo termina."""
    d0, n = e["data_concessao"], e["parcelas"]
    fim = {"para_em": None, "atraso_em": None,
           "atraso_dias": 0}
    if rng.random() < p:
        # deixa de pagar a parcela k e nunca mais paga
        k = int(rng.integers(1, min(n, 10) + 1))
        fim["para_em"] = d0 + timedelta(days=30 * k)
    elif rng.random() < 0.10 + 0.8 * p:
        # atrasa uma parcela e depois põe em dia
        j = int(rng.integers(1, n + 1))
        fim["atraso_em"] = d0 + timedelta(days=30 * j)
        fim["atraso_dias"] = int(rng.integers(5, 86))
    return fim


def situacao(e, f, hoje):
    """Como o sistema de cobrança vê o empréstimo em `hoje`."""
    d0, n = e["data_concessao"], e["parcelas"]
    ultima = d0 + timedelta(days=30 * n)
    s = {"pedido_id": e["pedido_id"], "situacao": "em dia",
         "dias_atraso_atual": 0, "data_atraso_30": None,
         "data_atraso_60": None, "data_atraso_90": None,
         "data_quitacao": None, "data_baixa": None}
    parou = f["para_em"]
    if parou is not None and parou <= hoje:
        dias = (hoje - parou).days
        for marco in (30, 60, 90):
            if dias >= marco:
                s[f"data_atraso_{marco}"] = (
                    parou + timedelta(marco))
        s["dias_atraso_atual"] = dias
        s["situacao"] = "atraso"
        if dias >= 360:
            s["situacao"] = "baixado"
            s["data_baixa"] = parou + timedelta(days=360)
        pagas = (parou - d0).days // 30 - 1
    else:
        pagas = min(n, max(0, (hoje - d0).days // 30))
        fim_atraso = None
        inicio = f["atraso_em"]
        if inicio is not None and inicio <= hoje:
            fim_atraso = inicio + timedelta(f["atraso_dias"])
            dias = min((hoje - inicio).days, f["atraso_dias"])
            for marco in (30, 60):
                if dias >= marco:
                    s[f"data_atraso_{marco}"] = (
                        inicio + timedelta(marco))
            if hoje < fim_atraso:
                s["dias_atraso_atual"] = dias
                s["situacao"] = "atraso"
        quitacao = max(ultima, fim_atraso or ultima)
        if quitacao <= hoje:
            s["situacao"] = "quitado"
            s["data_quitacao"] = quitacao
            pagas = n
    s["saldo_devedor"] = round(e["valor"] * (n - pagas) / n, 2)
    return s
