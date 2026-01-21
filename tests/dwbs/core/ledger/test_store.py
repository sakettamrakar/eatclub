import pytest
from uuid import uuid4
from datetime import datetime
from dwbs.core.ledger.store.memory import InMemoryLedgerStore
from dwbs.core.ledger.events.types import PurchaseEvent, PurchasePayload, MutationType, MutationSource, Explanation
from dwbs.core.identity.resolution import ItemIdentity
from dwbs.core.units.converter import Quantity, Unit

def test_ledger_append_and_retrieve():
    store = InMemoryLedgerStore()

    payload = PurchasePayload(
        item=ItemIdentity(name="Apple"),
        quantity=Quantity(value=1.0, unit=Unit.PIECE),
        source=MutationSource.USER_MANUAL,
        explanation=Explanation(reason="Init", source_fact="test", confidence=1.0)
    )
    event = PurchaseEvent(
        event_id=uuid4(),
        timestamp=datetime.now(),
        actor="tester",
        payload=payload
    )

    store.append(event)

    events = list(store.get_stream())
    assert len(events) == 1
    assert events[0] == event

    snapshot = store.snapshot()
    assert len(snapshot) == 1
    assert snapshot[0] == event

def test_ledger_immutability():
    store = InMemoryLedgerStore()

    payload = PurchasePayload(
        item=ItemIdentity(name="Apple"),
        quantity=Quantity(value=1.0, unit=Unit.PIECE),
        source=MutationSource.USER_MANUAL,
        explanation=Explanation(reason="Init", source_fact="test", confidence=1.0)
    )
    event = PurchaseEvent(
        event_id=uuid4(),
        timestamp=datetime.now(),
        actor="tester",
        payload=payload
    )
    store.append(event)

    snapshot = store.snapshot()
    snapshot.clear() # Modifying the snapshot list

    # Store should still have the event
    assert len(list(store.get_stream())) == 1
