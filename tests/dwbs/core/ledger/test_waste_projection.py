import pytest
from decimal import Decimal
from uuid import uuid4
from datetime import datetime
from dwbs.core.ledger.events.types import PurchaseEvent, PurchasePayload, WasteEvent, WastePayload, MutationType, MutationSource, Explanation
from dwbs.core.ledger.waste.reasons import WasteReason
from dwbs.core.units.converter import Quantity, Unit
from dwbs.core.identity.resolution import ItemIdentity
from dwbs.core.ledger.projection import InventoryProjector

def test_waste_reduces_inventory():
    item_id = ItemIdentity(name="Lettuce")

    # Buy 1KG
    buy = PurchaseEvent(
        event_id=uuid4(),
        timestamp=datetime.now(),
        actor="user",
        payload=PurchasePayload(
            item=item_id,
            quantity=Quantity(value=Decimal("1"), unit=Unit.KILOGRAM),
            source=MutationSource.USER_MANUAL,
            explanation=Explanation(reason="Bought", source_fact="manual", confidence=1.0)
        )
    )

    # Waste 500G
    waste = WasteEvent(
        event_id=uuid4(),
        timestamp=datetime.now(),
        actor="user",
        payload=WastePayload(
            item=item_id,
            quantity=Quantity(value=Decimal("500"), unit=Unit.GRAM),
            reason=WasteReason.SPILLED,
            source=MutationSource.USER_MANUAL,
            explanation=Explanation(reason="Spilled", source_fact="manual", confidence=1.0)
        )
    )

    final_state = InventoryProjector.project_state([buy, waste])

    assert "Lettuce" in final_state
    remaining = final_state["Lettuce"]
    assert remaining.unit == Unit.GRAM
    assert remaining.value == Decimal("500")
