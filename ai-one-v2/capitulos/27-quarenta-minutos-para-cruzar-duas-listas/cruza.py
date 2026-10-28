"""Duas maneiras de somar o consumo de cada cooperado."""


def por_lista(cpfs, linhas):
    """Para cada cooperado, varre todas as linhas."""
    totais = []
    for cpf in cpfs:
        soma = 0.0
        for linha_cpf, kwh in linhas:
            if linha_cpf == cpf:
                soma += kwh
        totais.append(soma)
    return totais


def por_dicionario(cpfs, linhas):
    """Uma passada só pelas linhas, somando num dicionário."""
    soma = dict.fromkeys(cpfs, 0.0)
    for linha_cpf, kwh in linhas:
        if linha_cpf in soma:
            soma[linha_cpf] += kwh
    return [soma[cpf] for cpf in cpfs]
