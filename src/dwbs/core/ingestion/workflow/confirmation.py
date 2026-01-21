from typing import List
from datetime import datetime
from ...ledger.store.interface import LedgerStore
from ...ledger.events.types import PurchaseEvent, PurchasePayload
from ...contracts.mutation import MutationSource
from ...contracts.explanation import Explanation
from ..draft.schema import DraftItem

class DraftConfirmationService:
    """
    D4.2 User Confirmation Loop
    Workflow logic to convert drafts into ledger events.
    """
    def __init__(self, ledger_store: LedgerStore):
        self.ledger_store = ledger_store

    def finalize_draft(self, draft_items: List[DraftItem], actor: str = "user") -> List[PurchaseEvent]:
        """
        Converts a list of confirmed draft items into PurchaseEvents and commits them to the ledger.
        """
        events = []
        for draft in draft_items:
            payload = PurchasePayload(
                item=draft.item,
                quantity=draft.quantity,
                expiry_date=draft.expiry_date,
                source=MutationSource.USER_CONFIRMED_OCR,
                explanation=Explanation(
                    reason="User confirmed draft item.",
                    source_fact="workflow:confirmation",
                    confidence=1.0
                )
            )

            event = PurchaseEvent(
                actor=actor,
                payload=payload
            )

            self.ledger_store.append(event)
            events.append(event)

        return events
