from decimal import Decimal

from app.precos import com_margem


def test_aplica_margem_padrao_de_doze_por_cento():
    assert com_margem(Decimal("10.00")) == Decimal("11.20")
