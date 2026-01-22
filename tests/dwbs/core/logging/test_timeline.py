import pytest
from decimal import Decimal
from src.dwbs.core.logging.timeline.logger import TimelineLogger
from src.dwbs.core.ledger.events.types import PurchaseEvent, PurchasePayload, MutationType
from src.dwbs.core.contracts.mutation import MutationSource
from src.dwbs.core.contracts.explanation import Explanation
from src.dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit

class TestTimelineLogger:
    def setup_method(self):
        self.logger = TimelineLogger()

    def test_log_purchase(self):
        event = PurchaseEvent(
            actor="Alice",
            payload=PurchasePayload(
                item=ItemIdentity(name="Milk"),
                quantity=Quantity(value=Decimal(1), unit=Unit.LITER),
                source=MutationSource.USER_MANUAL,
                explanation=Explanation(reason="test", source_fact="test", confidence=1.0)
            )
        )

        entry = self.logger.log_activity(event)
        assert entry is not None
        assert entry.actor == "Alice"
        assert entry.description == "Purchased Milk"
        assert entry.action_type == "PURCHASE"

    def test_log_unknown_actor(self):
        # LedgerEvent model requires actor, but let's assume it could be empty string?
        # Pydantic validation usually catches None.
        pass
