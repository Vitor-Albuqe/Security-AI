from datetime import date
from decimal import Decimal

import pytest

from security_ai.domain.value_objects import converter_data, converter_valor


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("R$ 1.234,56", Decimal("1234.56")),
        ("12,50", Decimal("12.50")),
        ("45.90", Decimal("45.90")),
        ("sem valor", None),
    ],
)
def test_converter_valor(texto, esperado):
    assert converter_valor(texto) == esperado


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("10/03/23 09:43:52", date(2023, 3, 10)),
        ("Emissão: 05/11/2022", date(2022, 11, 5)),
        ("2023-01-31", date(2023, 1, 31)),
        ("19/FEV/2023", date(2023, 2, 19)),
        ("32/13/2023", None),
        ("sem data", None),
    ],
)
def test_converter_data(texto, esperado):
    assert converter_data(texto) == esperado
