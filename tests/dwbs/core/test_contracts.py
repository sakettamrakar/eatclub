import pytest
from datetime import datetime, date, timedelta
from pydantic import ValidationError
from dwbs.core.contracts import Quantity, Unit, Bought, ItemIdentity, StockStatus, MutationType, MutationSource, Explanation
from dwbs.core.domain import InventoryItem
from dwbs.core.outcome import Outcome, ErrorCode

def test_quantity_non_negative():
    """Task 1.6: Verify Quantity prevents negative values."""
    q = Quantity(value=10, unit=Unit.GRAM)
    assert q.value == 10

    with pytest.raises(ValidationError):
        Quantity(value=-1, unit=Unit.GRAM)

def test_inventory_item_in_stock():
    """Task 1.6: Verify 'In Stock' logic."""
    identity = ItemIdentity(name="Apple")

    # Case 1: In stock
    item = InventoryItem(
        id="1",
        identity=identity,
        quantity=Quantity(value=5, unit=Unit.PIECE),
        status=StockStatus.IN_STOCK
    )
    assert item.is_in_stock() == True

    # Case 2: Zero quantity
    item_zero = InventoryItem(
        id="2",
        identity=identity,
        quantity=Quantity(value=0, unit=Unit.PIECE),
        status=StockStatus.IN_STOCK
    )
    assert item_zero.is_in_stock() == False

    # Case 3: Explicitly EXPIRED status
    item_expired = InventoryItem(
        id="3",
        identity=identity,
        quantity=Quantity(value=5, unit=Unit.PIECE),
        status=StockStatus.EXPIRED
    )
    assert item_expired.is_in_stock() == False

def test_outcome_wrapper():
    """Task 1.6: Verify Outcome wrapper."""
    # Success case
    ok = Outcome.ok(data="Success")
    assert ok.success == True
    assert ok.unwrap() == "Success"

    # Failure case
    fail = Outcome.fail(code=ErrorCode.MISSING_DATA, message="Data missing")
    assert fail.success == False
    assert fail.error_code == ErrorCode.MISSING_DATA

    with pytest.raises(RuntimeError):
        fail.unwrap()

def test_inventory_mutation_hierarchy():
    """Task 1.6: Verify Mutation hierarchy structure."""
    identity = ItemIdentity(name="Banana")
    q = Quantity(value=1, unit=Unit.BUNCH)

    # Bought
    bought = Bought(
        source=MutationSource.USER_MANUAL,
        item=identity,
        quantity=q
    )
    assert bought.mutation_type == MutationType.PURCHASE
    assert bought.source == MutationSource.USER_MANUAL

    # Verify Explanation contract (just instantiation)
    expl = Explanation(
        reason="Because I said so",
        source_fact="My Brain",
        confidence=1.0
    )
    assert expl.reason == "Because I said so"
