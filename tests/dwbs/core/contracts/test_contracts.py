import pytest
from datetime import date, timedelta
from pydantic import ValidationError

from dwbs.core.contracts.inventory import Quantity, Unit, InventoryItem, StockStatus, ItemIdentity
from dwbs.core.contracts.explanation import Explanation
from dwbs.core.contracts.failure import Result, ErrorCode
from dwbs.core.contracts.mutation import Bought, MutationType, MutationSource

def test_quantity_non_negative():
    """Verify that Quantity cannot be negative."""
    with pytest.raises(ValidationError):
        Quantity(value=-1, unit=Unit.GRAM)

    q = Quantity(value=10, unit=Unit.GRAM)
    assert q.value == 10

def test_quantity_normalization():
    """Verify unit normalization."""
    q = Quantity(value=1, unit=Unit.KILOGRAM)
    norm = q.normalize()
    assert norm.value == 1000
    assert norm.unit == Unit.GRAM

def test_inventory_item_in_stock():
    """Verify In Stock predicate."""
    item_id = ItemIdentity(name="Test Item")

    # Positive qty, no expiry
    item = InventoryItem(
        item=item_id,
        quantity=Quantity(value=1, unit=Unit.PIECE),
        status=StockStatus.IN_STOCK
    )
    assert item.is_in_stock()

    # Zero qty
    item_zero = item.model_copy(update={"quantity": Quantity(value=0, unit=Unit.PIECE)})
    assert not item_zero.is_in_stock()

    # Expired
    yesterday = date.today() - timedelta(days=1)
    item_expired = item.model_copy(update={"expiry_date": yesterday})
    assert not item_expired.is_in_stock()

def test_explanation_structure():
    """Verify Explanation fields."""
    exp = Explanation(
        reason="Test Reason",
        source_fact="Rule 1",
        confidence=0.9
    )
    assert exp.reason == "Test Reason"

    # Missing fields
    with pytest.raises(ValidationError):
        Explanation(reason="Missing Source")

def test_result_success_failure():
    """Verify Result wrapper."""
    res = Result.success("Success")
    assert res.is_success
    assert not res.is_failure
    assert res.value == "Success"

    fail = Result.fail(ErrorCode.MISSING_DATA, "Missing something")
    assert fail.is_failure
    assert not fail.is_success
    assert fail.error.code == ErrorCode.MISSING_DATA

def test_mutation_structure():
    """Verify Mutation inheritance."""
    mut = Bought(source=MutationSource.USER_MANUAL)
    assert mut.mutation_type == MutationType.PURCHASE
