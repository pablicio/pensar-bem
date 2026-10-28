@pytest.mark.parametrize(
    "caixas,esperado",
    [
        (1, Decimal("12.00")),
        (5, Decimal("28.00")),
        (40, Decimal("80.00")),
        (100, Decimal("80.00")),
    ],
)
def test_frete_por_faixa(caixas, esperado):
    assert frete(caixas) == esperado
