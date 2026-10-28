"""Números, valores e datas por extenso, como nos atos."""

UNIDADES = ("zero um dois três quatro cinco seis sete oito"
            " nove dez onze doze treze catorze quinze"
            " dezesseis dezessete dezoito dezenove").split()
DEZENAS = ("_ _ vinte trinta quarenta cinquenta sessenta"
           " setenta oitenta noventa").split()
CENTENAS = ("_ cento duzentos trezentos quatrocentos"
            " quinhentos seiscentos setecentos oitocentos"
            " novecentos").split()
MESES = ("janeiro fevereiro março abril maio junho julho"
         " agosto setembro outubro novembro dezembro").split()


def _ate_mil(n):
    """De 1 a 999."""
    if n == 100:
        return "cem"
    partes = []
    c, resto = divmod(n, 100)
    if c:
        partes.append(CENTENAS[c])
    if resto >= 20:
        d, u = divmod(resto, 10)
        partes.append(DEZENAS[d])
        if u:
            partes.append(UNIDADES[u])
    elif resto:
        partes.append(UNIDADES[resto])
    return " e ".join(partes)


def numero(n):
    """Um inteiro de 0 a 999.999.999 por extenso."""
    if n == 0:
        return "zero"
    milhoes, resto = divmod(n, 1_000_000)
    milhares, unidades = divmod(resto, 1000)
    partes = []
    if milhoes:
        nome = "milhão" if milhoes == 1 else "milhões"
        partes.append(f"{_ate_mil(milhoes)} {nome}")
    if milhares:
        partes.append("mil" if milhares == 1
                      else f"{_ate_mil(milhares)} mil")
    if unidades:
        partes.append(_ate_mil(unidades))
    if len(partes) == 1:
        return partes[0]
    # "e" antes da última parte quando ela é redonda ou
    # menor que cem: "mil e duzentos", "mil, duzentos e dez"
    ultima = unidades if unidades else milhares
    redonda = ultima < 100 or ultima % 100 == 0
    sep = " e " if redonda else ", "
    return ", ".join(partes[:-1]) + sep + partes[-1]


def reais(centavos):
    """'um milhão de reais', 'mil reais e dez centavos'."""
    r, c = divmod(centavos, 100)
    texto = ""
    if r:
        de = " de" if r % 1_000_000 == 0 else ""
        texto = numero(r) + de + (" real" if r == 1
                                  else " reais")
    if c:
        cent = numero(c) + (" centavo" if c == 1
                            else " centavos")
        texto = f"{texto} e {cent}" if texto else cent
    return texto


def valor(centavos):
    """R$ 1.234.567,89"""
    r, c = divmod(centavos, 100)
    return f"R$ {r:,}".replace(",", ".") + f",{c:02d}"


def data(d):
    """12 de março de 2026"""
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def data_por_extenso(d):
    """doze de março de dois mil e vinte e seis"""
    dia = "primeiro" if d.day == 1 else numero(d.day)
    return f"{dia} de {MESES[d.month - 1]} de {numero(d.year)}"
