"""Normalização e conferência de CPF."""


class CPFInvalido(ValueError):
    """Um CPF que não passa na conferência."""


def normaliza_cpf(cpf):
    """O CPF só com os onze dígitos, como texto."""
    texto = str(cpf).strip()
    for sinal in ".- ":
        texto = texto.replace(sinal, "")
    return texto.zfill(11)


def verificadores(nove):
    """Os dois dígitos finais, a partir dos nove primeiros."""
    d = [int(c) for c in nove]
    for n in (9, 10):
        soma = sum(v * (n + 1 - i) for i, v in enumerate(d))
        d.append(soma * 10 % 11 % 10)
    return d[9:]


def confere_cpf(cpf):
    """O CPF normalizado, ou CPFInvalido com o motivo."""
    texto = normaliza_cpf(cpf)
    if not texto.isdigit():
        raise CPFInvalido(f"tem letra ou sinal: {cpf!r}")
    if len(texto) != 11:
        raise CPFInvalido(f"não tem 11 dígitos: {cpf!r}")
    fim = [int(c) for c in texto[9:]]
    if verificadores(texto[:9]) != fim:
        raise CPFInvalido(f"verificador errado: {cpf!r}")
    return texto
