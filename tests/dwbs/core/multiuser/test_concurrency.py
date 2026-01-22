import pytest
from decimal import Decimal
from src.dwbs.core.ledger.store.memory import InMemoryLedgerStore
from src.dwbs.core.ledger.events.types import PurchaseEvent, PurchasePayload, MutationType
from src.dwbs.core.contracts.mutation import MutationSource
from src.dwbs.core.contracts.explanation import Explanation
from src.dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit
from src.dwbs.core.exceptions import ConcurrencyError

class TestMultiUserConcurrency:
    """
    P2-T23: Validate Multi-User Concurrency
    Simulate 2 users editing same item. Verify locking and resolution.
    """

    def setup_method(self):
        self.ledger = InMemoryLedgerStore()

    def create_event(self, actor: str, version: int = None) -> PurchaseEvent:
        return PurchaseEvent(
            actor=actor,
            expected_version=version,
            payload=PurchasePayload(
                item=ItemIdentity(name="Apple"),
                quantity=Quantity(value=Decimal(1), unit=Unit.PIECE),
                source=MutationSource.USER_MANUAL,
                explanation=Explanation(reason="test", source_fact="test", confidence=1.0)
            )
        )

    def test_optimistic_locking_collision(self):
        # Initial state version is 0
        current_version = self.ledger.version
        assert current_version == 0

        # User A reads version 0 and prepares event
        event_A = self.create_event("UserA", version=0)

        # User B reads version 0 and prepares event
        event_B = self.create_event("UserB", version=0)

        # User A commits first -> Success
        self.ledger.append(event_A)
        assert self.ledger.version == 1

        # User B tries to commit with expected_version=0 -> Failure
        with pytest.raises(ConcurrencyError) as excinfo:
            self.ledger.append(event_B)

        assert "Version mismatch" in str(excinfo.value)

    def test_sequential_edits(self):
        # User A commits
        event_A = self.create_event("UserA", version=0)
        self.ledger.append(event_A)

        # User B reads updated version (1)
        event_B = self.create_event("UserB", version=1)
        self.ledger.append(event_B)

        assert self.ledger.version == 2
