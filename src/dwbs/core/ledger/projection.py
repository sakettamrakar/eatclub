from typing import List, Dict, Any
from decimal import Decimal
from .events.types import LedgerEvent, PurchaseEvent, ConsumeEvent, WasteEvent, CorrectionAddEvent, CorrectionRemoveEvent
from ..units.converter import Quantity, Unit

class InventoryProjector:
    """
    Projector service that reconstructs the current state of inventory from the event stream.
    """

    @staticmethod
    def project_state(events: List[LedgerEvent]) -> Dict[str, Quantity]:
        """
        Reconstructs the current inventory state (Item Name -> Quantity).
        Normalizes all quantities to their base unit for aggregation.
        """
        inventory: Dict[str, Quantity] = {} # name -> Quantity (normalized)

        for event in events:
            # Skip events without payload or quantity if any (e.g. unknown types)
            if not hasattr(event, 'payload') or not hasattr(event.payload, 'quantity'):
                continue

            qty = event.payload.quantity.normalize()
            item_name = event.payload.item.name

            # Helper to get current value or 0
            current_qty = inventory.get(item_name)

            if isinstance(event, (PurchaseEvent, CorrectionAddEvent)):
                if current_qty is None:
                    inventory[item_name] = qty
                else:
                    inventory[item_name] = current_qty + qty

            elif isinstance(event, (ConsumeEvent, WasteEvent, CorrectionRemoveEvent)):
                if current_qty is not None:
                    # Subtract
                    inventory[item_name] = current_qty - qty

                    # If quantity becomes <= 0, should we remove it?
                    # Contracts say "No negative inventory".
                    # If we go negative here, it means the ledger has invalid state relative to this simple projection.
                    # We will allow negative in calculation but maybe filter in UI.
                    # Or strictly, we keep it to show the discrepancy.
                else:
                    # Removing from empty?
                    # Initialize with negative
                    neg_qty = Quantity(value=-qty.value, unit=qty.unit, approx=qty.approx)
                    inventory[item_name] = neg_qty

        return inventory
