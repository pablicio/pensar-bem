def fator_capacidade(kwh, potencia_kw, horas=24):
    """Energia gerada sobre o máximo possível, em %."""
    return round(kwh / (potencia_kw * horas) * 100, 1)


assert fator_capacidade(7772, 2500) == 13.0
assert fator_capacidade(1000, 100, horas=10) == 100.0
print(fator_capacidade(7772, 2500))
