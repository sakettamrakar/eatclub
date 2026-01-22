import pytest
from decimal import Decimal
from src.dwbs.core.notifications.notifier import Notifier
from src.dwbs.core.ledger.events.types import PurchaseEvent, PurchasePayload, MutationType
from src.dwbs.core.contracts.mutation import MutationSource
from src.dwbs.core.contracts.explanation import Explanation
from src.dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit

class TestNotifier:
    def setup_method(self):
        self.notifier = Notifier()

    def test_notify_other_user_action(self):
        event = PurchaseEvent(
            actor="Alice",
            payload=PurchasePayload(
                item=ItemIdentity(name="Milk"),
                quantity=Quantity(value=Decimal(1), unit=Unit.LITER),
                source=MutationSource.USER_MANUAL,
                explanation=Explanation(reason="test", source_fact="test", confidence=1.0)
            )
        )

        notification = self.notifier.generate_notification(event, "Bob")
        assert notification is not None
        assert "Alice added Milk" in notification.body

    def test_no_notify_self_action(self):
        event = PurchaseEvent(
            actor="Alice",
            payload=PurchasePayload(
                item=ItemIdentity(name="Milk"),
                quantity=Quantity(value=Decimal(1), unit=Unit.LITER),
                source=MutationSource.USER_MANUAL,
                explanation=Explanation(reason="test", source_fact="test", confidence=1.0)
            )
        )

        notification = self.notifier.generate_notification(event, "Alice")
        assert notification is None
