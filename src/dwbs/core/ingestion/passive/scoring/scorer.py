from typing import List
from ...draft.schema import DraftItem
from ....contracts.inventory import ItemIdentity

class ConfidenceScorer:
    """
    D7.4 Confidence scoring
    Assigns confidence to Parsed Items based on source reliability.
    """

    KNOWN_VENDORS = {
        "orders@grocery.com",
        "receipts@supermarket.com",
        "store.com", # Domain matching logic?
        "amazon.com",
        "instacart.com"
    }

    def score_drafts(self, items: List[DraftItem], sender: str) -> List[DraftItem]:
        """
        Returns a new list of DraftItems with updated confidence scores.
        """
        confidence = self._calculate_confidence(sender)

        scored_items = []
        for draft in items:
            # Create new ItemIdentity with updated confidence
            original_identity = draft.item
            new_identity = ItemIdentity(
                name=original_identity.name,
                variant=original_identity.variant,
                brand=original_identity.brand,
                confidence=confidence
            )

            # Create new DraftItem
            scored_items.append(DraftItem(
                item=new_identity,
                quantity=draft.quantity,
                expiry_date=draft.expiry_date
            ))

        return scored_items

    def _calculate_confidence(self, sender: str) -> float:
        if not sender:
            return 0.1

        sender_lower = sender.lower()

        # Exact or partial match for known vendors
        for vendor in self.KNOWN_VENDORS:
            if vendor in sender_lower:
                return 0.9

        # Unknown vendor but successfully parsed
        return 0.3
