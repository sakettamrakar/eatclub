import pytest
from src.dwbs.core.ledger.sync.conflict_resolver import ConflictResolver, ResolutionChoice
from src.dwbs.core.ledger.events.types import PurchaseEvent, PurchasePayload, MutationType
from src.dwbs.core.contracts.mutation import MutationSource
from src.dwbs.core.contracts.explanation import Explanation
from src.dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit
from decimal import Decimal

class TestConflictResolver:
    def setup_method(self):
        self.resolver = ConflictResolver()

    def create_event(self, actor: str) -> PurchaseEvent:
        return PurchaseEvent(
            actor=actor,
            payload=PurchasePayload(
                item=ItemIdentity(name="Apple"),
                quantity=Quantity(value=Decimal(1), unit=Unit.PIECE),
                source=MutationSource.USER_MANUAL,
                explanation=Explanation(reason="test", source_fact="test", confidence=1.0)
            )
        )

    def test_keep_local(self):
        local_event = self.create_event("me")
        remote_event = self.create_event("them")

        result = self.resolver.resolve_conflict(local_event, remote_event, ResolutionChoice.KEEP_LOCAL)
        assert result.is_success
        assert result.value.actor == "me"

    def test_accept_remote(self):
        local_event = self.create_event("me")
        remote_event = self.create_event("them")

        result = self.resolver.resolve_conflict(local_event, remote_event, ResolutionChoice.ACCEPT_REMOTE)
        assert result.is_success
        assert result.value.actor == "them"
