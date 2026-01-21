import pytest
import time
import random
from decimal import Decimal
from uuid import uuid4
from datetime import datetime, date
from dwbs.core.ledger.events.types import PurchaseEvent, PurchasePayload, ConsumeEvent, ConsumePayload, WasteEvent, WastePayload, MutationType, MutationSource, Explanation
from dwbs.core.ledger.waste.reasons import WasteReason
from dwbs.core.units.converter import Quantity, Unit
from dwbs.core.identity.resolution import ItemIdentity
from dwbs.core.ledger.store.memory import InMemoryLedgerStore
from dwbs.core.ledger.projection import InventoryProjector

def test_ledger_reconstruction_performance_and_accuracy():
    store = InMemoryLedgerStore()
    expected_sum = Decimal(0)

    # Setup: 100 events
    # We'll stick to one item "TestItem" to make math easy to check.

    # 1. Initial Buy (Large enough to avoid negative stock during random walk)
    initial_qty = Decimal("100000") # 100 KG
    buy = PurchaseEvent(
        event_id=uuid4(),
        timestamp=datetime.now(),
        actor="setup",
        payload=PurchasePayload(
            item=ItemIdentity(name="TestItem"),
            quantity=Quantity(value=initial_qty, unit=Unit.GRAM),
            source=MutationSource.USER_MANUAL,
            explanation=Explanation(reason="Init", source_fact="test", confidence=1.0)
        )
    )
    store.append(buy)
    expected_sum += initial_qty

    random.seed(42) # Deterministic randomness

    for _ in range(99):
        # Randomly Buy, Consume, or Waste
        action = random.choice(["buy", "consume", "waste"])
        qty_val = Decimal(random.randint(1, 100))
        qty = Quantity(value=qty_val, unit=Unit.GRAM)

        evt = None
        if action == "buy":
            evt = PurchaseEvent(
                 event_id=uuid4(),
                 timestamp=datetime.now(),
                 actor="test",
                 payload=PurchasePayload(
                     item=ItemIdentity(name="TestItem"),
                     quantity=qty,
                     source=MutationSource.USER_MANUAL,
                     explanation=Explanation(reason="buy", source_fact="test", confidence=1.0)
                 )
            )
            expected_sum += qty_val
        elif action == "consume":
            evt = ConsumeEvent(
                 event_id=uuid4(),
                 timestamp=datetime.now(),
                 actor="test",
                 payload=ConsumePayload(
                     item=ItemIdentity(name="TestItem"),
                     quantity=qty,
                     source=MutationSource.USER_MANUAL,
                     explanation=Explanation(reason="eat", source_fact="test", confidence=1.0)
                 )
            )
            expected_sum -= qty_val
        elif action == "waste":
            evt = WasteEvent(
                 event_id=uuid4(),
                 timestamp=datetime.now(),
                 actor="test",
                 payload=WastePayload(
                     item=ItemIdentity(name="TestItem"),
                     quantity=qty,
                     reason=WasteReason.OTHER,
                     source=MutationSource.USER_MANUAL,
                     explanation=Explanation(reason="bad", source_fact="test", confidence=1.0)
                 )
            )
            expected_sum -= qty_val

        store.append(evt)

    # Reconstruction
    recon_start = time.time()
    events = store.snapshot()

    # Using the new service
    state = InventoryProjector.project_state(events)

    recon_end = time.time()

    # Assertions
    assert "TestItem" in state
    assert state["TestItem"].value == expected_sum
    assert state["TestItem"].unit == Unit.GRAM

    duration_ms = (recon_end - recon_start) * 1000
    print(f"Reconstruction took {duration_ms:.2f}ms")
    assert duration_ms < 100 # Requirement
