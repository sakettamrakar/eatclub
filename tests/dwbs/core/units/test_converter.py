import pytest
from decimal import Decimal
from dwbs.core.units.converter import Quantity, Unit

def test_normalization():
    q1 = Quantity(value=Decimal("1.5"), unit=Unit.KILOGRAM)
    q2 = q1.normalize()
    assert q2.value == Decimal("1500")
    assert q2.unit == Unit.GRAM

    q3 = Quantity(value=Decimal("0.5"), unit=Unit.LITER)
    q4 = q3.normalize()
    assert q4.value == Decimal("500")
    assert q4.unit == Unit.MILLILITER

def test_addition():
    q1 = Quantity(value=Decimal("500"), unit=Unit.GRAM)
    q2 = Quantity(value=Decimal("0.5"), unit=Unit.KILOGRAM)
    q3 = q1 + q2
    assert q3.value == Decimal("1000")
    assert q3.unit == Unit.GRAM

    # Approx propagation
    q4 = Quantity(value=Decimal("1"), unit=Unit.GRAM, approx=True)
    q5 = q1 + q4
    assert q5.approx is True

def test_incompatible_units():
    q1 = Quantity(value=Decimal("1"), unit=Unit.GRAM)
    q2 = Quantity(value=Decimal("1"), unit=Unit.LITER)
    with pytest.raises(ValueError):
        _ = q1 + q2

def test_decimal_precision():
    # 0.1 + 0.2 = 0.3
    q1 = Quantity(value=Decimal("0.1"), unit=Unit.GRAM)
    q2 = Quantity(value=Decimal("0.2"), unit=Unit.GRAM)
    q3 = q1 + q2
    assert q3.value == Decimal("0.3")
