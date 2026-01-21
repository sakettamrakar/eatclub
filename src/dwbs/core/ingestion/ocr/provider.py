from typing import List
from abc import ABC, abstractmethod
from ..draft.schema import DraftItem, DraftSession
from ...contracts.inventory import ItemIdentity, Quantity, Unit

class OcrProvider(ABC):
    """
    D4.3 OCR Extraction
    Interface for OCR providers.
    """
    @abstractmethod
    def process_image(self, image_data: bytes, session_id: str) -> DraftSession:
        pass

class MockOcrProvider(OcrProvider):
    """
    Mock implementation for Phase 1 Kernel.
    Returns hardcoded drafts with low confidence.
    """
    def process_image(self, image_data: bytes, session_id: str) -> DraftSession:
        # Simulate extracted items
        items = [
            DraftItem(
                item=ItemIdentity(name="Tomato", confidence=0.4),
                quantity=Quantity(value=2.0, unit=Unit.PIECE),
                expiry_date=None
            ),
            DraftItem(
                item=ItemIdentity(name="Milk", confidence=0.4),
                quantity=Quantity(value=1.0, unit=Unit.LITER),
                expiry_date=None
            )
        ]

        return DraftSession(
            session_id=session_id,
            items=items,
            source="MockOCR"
        )
