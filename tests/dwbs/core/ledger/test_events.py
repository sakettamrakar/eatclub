import pytest
from uuid import uuid4
from datetime import datetime, date
from dwbs.core.ledger.events.types import PurchaseEvent, PurchasePayload, MutationType, MutationSource, Explanation
from dwbs.core.identity.resolution import ItemIdentity
from dwbs.core.units.converter import Quantity, Unit

def test_purchase_event_serialization():
    item = ItemIdentity(name="Tomato", variant="Fresh")
    qty = Quantity(value=1.0, unit=Unit.KILOGRAM)
    explanation = Explanation(reason="Bought", source_fact="manual", confidence=1.0)

    payload = PurchasePayload(
        item=item,
        quantity=qty,
        expiry_date=date(2023, 1, 1),
        source=MutationSource.USER_MANUAL,
        explanation=explanation
    )

    event = PurchaseEvent(
        event_id=uuid4(),
        timestamp=datetime.now(),
        actor="user",
        payload=payload
    )

    json_str = event.model_dump_json()
    reconstructed = PurchaseEvent.model_validate_json(json_str)

    assert reconstructed.event_id == event.event_id
    assert reconstructed.payload.item.name == "Tomato"
    assert reconstructed.mutation_type == MutationType.PURCHASE
    assert reconstructed.payload.quantity.value == 1.0
