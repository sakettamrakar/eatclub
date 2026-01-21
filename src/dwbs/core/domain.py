from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, Field
from .contracts import SystemContract, StockStatus, Quantity, ItemIdentity, Unit

class InventoryItem(SystemContract):
    """
    D0.1 Inventory State Contract
    Represents an item in the inventory.
    """
    id: str = Field(..., description="Unique identifier for this specific inventory lot.")
    identity: ItemIdentity = Field(..., description="The type of item.")
    quantity: Quantity = Field(..., description="The amount remaining.")
    expiry_date: Optional[date] = Field(None, description="Expiration date.")
    purchase_date: Optional[datetime] = Field(None, description="When it was added.")
    status: StockStatus = Field(StockStatus.UNKNOWN, description="Current stock status.")

    def is_in_stock(self) -> bool:
        """
        D0.1: Strictly define what "In Stock" means.
        Quantity > 0 AND NOT expired (if expiry known).
        """
        if self.quantity.value <= 0:
            return False

        if self.status in (StockStatus.EXPIRED, StockStatus.OUT_OF_STOCK):
            return False

        return True

class InventoryState(SystemContract):
    """
    D0.1 Inventory State Contract
    Snapshot of the entire inventory.
    """
    items: List[InventoryItem] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.now)
    snapshot_id: str = Field(..., description="Unique ID for this state version.")
