"""A regra do rateio."""

TARIFA = 0.9412          # R$ por kWh compensado


def credito(geracao, cota_pct, tarifa=TARIFA):
    """kWh e R$ de uma cota (%) sobre a geração (kWh)."""
    kwh = round(geracao * cota_pct / 100, 2)
    return kwh, round(kwh * tarifa, 2)


def sobra(geracao, creditos, tarifa=TARIFA):
    """R$ que o arredondamento deixa numa usina; pelo
    regulamento, vai para a sede."""
    return round(geracao * tarifa - sum(creditos), 2)
