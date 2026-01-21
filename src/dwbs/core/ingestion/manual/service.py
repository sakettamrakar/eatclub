from typing import Optional
from datetime import date
from ...ledger.store.interface import LedgerStore
from ...ledger.events.types import PurchaseEvent, PurchasePayload
from ...contracts.mutation import MutationSource
from ...contracts.explanation import Explanation
from ...contracts.inventory import ItemIdentity, Quantity

class ManualEntryService:
    """
    D4.4 Manual Add/Edit UI
    Service for direct manual entry of inventory items.
    """
    def __init__(self, ledger_store: LedgerStore):
        self.ledger_store = ledger_store

    def create_entry(self, item: ItemIdentity, quantity: Quantity, expiry_date: Optional[date] = None, actor: str = "user") -> PurchaseEvent:
        """
        Creates a high-confidence purchase event for a manually entered item.
        """
        # Enforce high confidence for manual entry
        if item.confidence != 1.0:
            # We treat manual entry as truth. Create a new identity with 1.0 confidence or update it.
            item = item.model_copy(update={"confidence": 1.0})

        payload = PurchasePayload(
            item=item,
            quantity=quantity,
            expiry_date=expiry_date,
            source=MutationSource.USER_MANUAL,
            explanation=Explanation(
                reason="Manual entry by user.",
                source_fact="ingestion:manual",
                confidence=1.0
            )
        )

        event = PurchaseEvent(
            actor=actor,
            payload=payload
        )

        self.ledger_store.append(event)
        return event
