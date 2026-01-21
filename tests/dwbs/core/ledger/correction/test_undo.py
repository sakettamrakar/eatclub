import pytest
from decimal import Decimal
from src.dwbs.core.ledger.store.memory import InMemoryLedgerStore
from src.dwbs.core.ledger.events.types import ConsumeEvent, ConsumePayload, PurchaseEvent, PurchasePayload, CorrectionAddEvent
from src.dwbs.core.contracts.mutation import MutationSource
from src.dwbs.core.contracts.explanation import Explanation
from src.dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit
from src.dwbs.core.ledger.correction.undo import UndoService

class TestUndoService:
    def setup_method(self):
        self.ledger = InMemoryLedgerStore()
        self.service = UndoService()

    def create_consume_event(self, item_name: str, qty: int) -> ConsumeEvent:
        return ConsumeEvent(
            actor="user",
            payload=ConsumePayload(
                item=ItemIdentity(name=item_name),
                quantity=Quantity(value=Decimal(qty), unit=Unit.PIECE),
                source=MutationSource.USER_MANUAL,
                explanation=Explanation(reason="test", source_fact="test", confidence=1.0)
            )
        )

    def test_undo_last_consumption(self):
        event = self.create_consume_event("Apple", 1)
        self.ledger.append(event)

        result = self.service.undo_consumption(self.ledger, str(event.event_id), "user")
        assert result.is_success
        correction = result.value
        assert isinstance(correction, CorrectionAddEvent)
        assert correction.payload.item.name == "Apple"
        assert correction.payload.quantity_delta.value == Decimal("1")

    def test_block_undo_if_modified(self):
        event1 = self.create_consume_event("Apple", 1)
        self.ledger.append(event1)

        event2 = self.create_consume_event("Apple", 1) # Another consumption of same item
        self.ledger.append(event2)

        # Try to undo first event
        result = self.service.undo_consumption(self.ledger, str(event1.event_id), "user")
        assert result.is_failure
        assert "modified since" in result.error.message

    def test_allow_undo_if_other_item_modified(self):
        event1 = self.create_consume_event("Apple", 1)
        self.ledger.append(event1)

        event2 = self.create_consume_event("Banana", 1)
        self.ledger.append(event2)

        result = self.service.undo_consumption(self.ledger, str(event1.event_id), "user")
        assert result.is_success
