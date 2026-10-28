def normaliza_cpf(cpf):
    """O CPF só com os onze dígitos, como texto."""
    texto = str(cpf).strip()
    for sinal in ".- ":
        texto = texto.replace(sinal, "")
    return texto.zfill(11)


def credito(geracao, cota, tarifa=0.9412):
    """Crédito de um cooperado em kWh e em reais."""
    kwh = round(geracao * cota / 100, 2)
    return kwh, round(kwh * tarifa, 2)


if __name__ == "__main__":
    assert normaliza_cpf("060.419.765-98") == "06041976598"
    assert normaliza_cpf(6041976598) == "06041976598"
    assert credito(126809.824, 1.3954) == (1769.5, 1665.45)
    print("todas as conferências passaram")
