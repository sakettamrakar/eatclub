import pytest
from datetime import date, timedelta
from dwbs.core.ledger import InventoryLedger, InventoryEvent
from dwbs.core.domain import ItemIdentity, Quantity, Unit
from dwbs.core.contracts import MutationType, MutationSource, Explanation
from dwbs.core.exceptions import InvalidInventoryStateError

@pytest.fixture
def ledger():
    return InventoryLedger()

@pytest.fixture
def item_tomato():
    return ItemIdentity(name="Tomato", variant="Fresh")

@pytest.fixture
def explanation():
    return Explanation(summary="Test", source_rule="Test", confidence_score=1.0)

def test_purchase_and_state(ledger, item_tomato, explanation):
    event = InventoryEvent(
        item=item_tomato,
        quantity=Quantity(value=1, unit=Unit.KILOGRAM),
        mutation_type=MutationType.PURCHASE,
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    )
    ledger.append(event)

    state = ledger.get_current_state()
    assert len(state) == 1
    assert state[0].item == item_tomato
    assert state[0].quantity.value == 1
    assert state[0].quantity.unit == Unit.KILOGRAM

def test_consume_partial(ledger, item_tomato, explanation):
    # Purchase 1KG
    ledger.append(InventoryEvent(
        item=item_tomato,
        quantity=Quantity(value=1, unit=Unit.KILOGRAM),
        mutation_type=MutationType.PURCHASE,
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    ))

    # Consume 500G
    ledger.append(InventoryEvent(
        item=item_tomato,
        quantity=Quantity(value=500, unit=Unit.GRAM),
        mutation_type=MutationType.CONSUME,
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    ))

    state = ledger.get_current_state()
    assert len(state) == 1
    # Should be 500G remaining (normalized to G because operation converts to smaller unit usually, or keeps one)
    # Our implementation converts to LHS unit in arithmetic.
    # 1 KG - 500 G = 500 G.
    assert state[0].quantity.value == 500
    assert state[0].quantity.unit == Unit.GRAM

def test_prevent_negative_inventory(ledger, item_tomato, explanation):
    # Purchase 100G
    ledger.append(InventoryEvent(
        item=item_tomato,
        quantity=Quantity(value=100, unit=Unit.GRAM),
        mutation_type=MutationType.PURCHASE,
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    ))

    # Try to consume 200G
    with pytest.raises(InvalidInventoryStateError):
        ledger.append(InventoryEvent(
            item=item_tomato,
            quantity=Quantity(value=200, unit=Unit.GRAM),
            mutation_type=MutationType.CONSUME,
            source=MutationSource.USER_MANUAL,
            explanation=explanation
        ))

def test_waste_event(ledger, item_tomato, explanation):
    # Purchase 1KG
    ledger.append(InventoryEvent(
        item=item_tomato,
        quantity=Quantity(value=1, unit=Unit.KILOGRAM),
        mutation_type=MutationType.PURCHASE,
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    ))

    # Waste 1KG
    ledger.append(InventoryEvent(
        item=item_tomato,
        quantity=Quantity(value=1, unit=Unit.KILOGRAM),
        mutation_type=MutationType.WASTE,
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    ))

    state = ledger.get_current_state()
    assert len(state) == 0

def test_correction_add_remove(ledger, item_tomato, explanation):
    # Purchase 100G
    ledger.append(InventoryEvent(
        item=item_tomato,
        quantity=Quantity(value=100, unit=Unit.GRAM),
        mutation_type=MutationType.PURCHASE,
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    ))

    # Correct: Add 50G (Found more)
    ledger.append(InventoryEvent(
        item=item_tomato,
        quantity=Quantity(value=50, unit=Unit.GRAM),
        mutation_type=MutationType.CORRECTION_ADD,
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    ))

    state = ledger.get_current_state()
    assert state[0].quantity.value == 150

    # Correct: Remove 20G (Counted wrong)
    ledger.append(InventoryEvent(
        item=item_tomato,
        quantity=Quantity(value=20, unit=Unit.GRAM),
        mutation_type=MutationType.CORRECTION_REMOVE,
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    ))

    state = ledger.get_current_state()
    assert state[0].quantity.value == 130
