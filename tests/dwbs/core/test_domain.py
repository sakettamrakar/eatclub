import pytest
from dwbs.core.domain import Quantity, Unit, ItemIdentity

def test_quantity_normalization():
    q1 = Quantity(value=1.5, unit=Unit.KILOGRAM)
    norm_q1 = q1.normalize()
    assert norm_q1.value == 1500
    assert norm_q1.unit == Unit.GRAM

    q2 = Quantity(value=500, unit=Unit.GRAM)
    norm_q2 = q2.normalize()
    assert norm_q2.value == 500
    assert norm_q2.unit == Unit.GRAM

def test_quantity_arithmetic():
    q1 = Quantity(value=100, unit=Unit.GRAM)
    q2 = Quantity(value=50, unit=Unit.GRAM)

    q3 = q1 + q2
    assert q3.value == 150
    assert q3.unit == Unit.GRAM

    q4 = q1 - q2
    assert q4.value == 50
    assert q4.unit == Unit.GRAM

def test_quantity_arithmetic_mixed_units():
    q1 = Quantity(value=1, unit=Unit.KILOGRAM)
    q2 = Quantity(value=500, unit=Unit.GRAM)

    q3 = q1 + q2
    assert q3.value == 1500
    assert q3.unit == Unit.GRAM

    q4 = q1 - q2
    assert q4.value == 500
    assert q4.unit == Unit.GRAM

def test_quantity_comparison():
    q1 = Quantity(value=1, unit=Unit.KILOGRAM)
    q2 = Quantity(value=500, unit=Unit.GRAM)

    assert q2 < q1
    assert q1 > q2
    assert q1 == Quantity(value=1000, unit=Unit.GRAM)

def test_quantity_negative_value():
    with pytest.raises(ValueError):
        Quantity(value=-1, unit=Unit.GRAM)

def test_item_identity():
    item = ItemIdentity(name="Tomato", variant="Canned")
    assert item.full_name() == "Tomato (Canned)"

    item2 = ItemIdentity(name="Milk", brand="Amul")
    assert item2.full_name() == "Milk [Amul]"
