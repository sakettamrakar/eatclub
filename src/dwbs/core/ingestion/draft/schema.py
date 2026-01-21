from typing import List, Optional
from datetime import date
from pydantic import Field
from ...contracts.base import SystemContract
from ...contracts.inventory import ItemIdentity, Quantity, StockStatus

class DraftItem(SystemContract):
    """
    D4.1 Draft State Flow
    Represents an item that is being prepared for ingestion but not yet committed to ledger.
    """
    item: ItemIdentity
    quantity: Quantity
    expiry_date: Optional[date] = Field(None, description="Expiry date if detected.")

class DraftSession(SystemContract):
    """
    D4.1 Draft State Flow
    A session of draft items (e.g. from one receipt scan).
    """
    session_id: str = Field(..., description="Unique identifier for the session.")
    items: List[DraftItem]
    source: str = Field(..., description="Source of draft (e.g. OCR, Manual)")
