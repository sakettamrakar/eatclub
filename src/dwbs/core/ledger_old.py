from datetime import datetime, date
from typing import List, Optional, Dict
from uuid import UUID, uuid4
from pydantic import Field

from .contracts import (
    SystemContract, MutationType, MutationSource, Explanation, StockStatus
)
from .domain import ItemIdentity, Quantity, Unit
from .exceptions import InvalidInventoryStateError, MutationError

class InventoryEvent(SystemContract):
    """
    D1.1 Event-Sourcing Lite
    Immutable record of a change to the inventory.
    """
    event_id: UUID = Field(default_factory=uuid4, description="Unique event ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the event occurred")

    item: ItemIdentity = Field(..., description="The item being affected")
    quantity: Quantity = Field(..., description="The quantity involved in the event (absolute value)")

    mutation_type: MutationType = Field(..., description="Type of operation")
    source: MutationSource = Field(..., description="Who authorized this")

    # D1.5 Expiry & Purchase Tracking
    expiry_date: Optional[date] = Field(None, description="Expiry date of the batch (relevant for PURCHASE)")

    explanation: Explanation = Field(..., description="Why this event happened")

class InventoryItem(SystemContract):
    """
    Represents the current state of an item in the inventory.
    """
    item: ItemIdentity
    quantity: Quantity
    expiry_date: Optional[date] = None
    status: StockStatus = StockStatus.IN_STOCK

class InventoryLedger:
    """
    D1.1 Event-Sourcing Lite
    The single source of truth for inventory state.
    """
    def __init__(self):
        self._events: List[InventoryEvent] = []

    def append(self, event: InventoryEvent):
        """
        Appends a new event to the ledger.
        Validates that the event does not violate invariants (e.g. negative stock).
        """
        # We might want to check for negative inventory here or during reconstruction.
        # D1 Acceptance: "No negative quantities".
        # To enforce this strictly, we should probably check current state before appending consumption.

        if event.mutation_type in [MutationType.CONSUME, MutationType.WASTE, MutationType.CORRECTION_REMOVE]:
             # Check if we have enough stock
             current_state = self.get_current_state()
             # Find matching item (simplified for now, ideally by ID or hash)
             # Here we match by ItemIdentity equality

             available_qty = None
             for inv_item in current_state:
                 if inv_item.item == event.item:
                     # For now, simplistic aggregation of batches.
                     # Real system might track batches separately.
                     if available_qty is None:
                         available_qty = inv_item.quantity
                     else:
                         available_qty += inv_item.quantity

             if available_qty is None:
                 raise InvalidInventoryStateError(f"Cannot remove {event.item.full_name()}: Item not in inventory.")

             elif event.quantity > available_qty:
                  raise InvalidInventoryStateError(
                      f"Cannot remove {event.quantity.value} {event.quantity.unit} of {event.item.full_name()}: Only {available_qty.value} {available_qty.unit} available."
                  )

        self._events.append(event)

    def get_events(self) -> List[InventoryEvent]:
        """Return a copy of events."""
        return list(self._events)

    def get_current_state(self) -> List[InventoryItem]:
        """
        Reconstructs the current inventory state from the event log.
        """
        inventory: Dict[str, InventoryItem] = {}

        for event in self._events:
            # Key by item properties for now. In a real DB, this would be an ID.
            # Using JSON dump as a quick hashable key for the object
            key = event.item.model_dump_json()

            if key not in inventory:
                if event.mutation_type in [MutationType.PURCHASE, MutationType.CORRECTION_ADD]:
                    inventory[key] = InventoryItem(
                        item=event.item,
                        quantity=event.quantity,
                        expiry_date=event.expiry_date
                    )
                else:
                    # Consuming/Removing something that doesn't exist in reconstruction logic
                    # This shouldn't happen if append validation works, but good to handle.
                    pass
            else:
                current_item = inventory[key]

                # Normalize quantities for arithmetic
                # Note: We are assuming single batch tracking per item-variant for simplicity in Phase 1 start.
                # Complex batch tracking (FIFO/LIFO) would require a list of batches per item.

                new_quantity = current_item.quantity
                new_expiry = current_item.expiry_date

                if event.mutation_type in [MutationType.PURCHASE, MutationType.CORRECTION_ADD]:
                    new_quantity = new_quantity + event.quantity
                    # Update expiry if new one is sooner? or keep separate batches?
                    # Phase 1: Simple aggregation. We might overwrite expiry or keep the nearest one.
                    # Let's keep the nearest expiry date to be safe (conservative).
                    if event.expiry_date:
                        if new_expiry is None or event.expiry_date < new_expiry:
                            new_expiry = event.expiry_date

                elif event.mutation_type in [MutationType.CONSUME, MutationType.WASTE, MutationType.CORRECTION_REMOVE]:
                    new_quantity = new_quantity - event.quantity

                inventory[key] = current_item.model_copy(update={"quantity": new_quantity, "expiry_date": new_expiry})

        # Filter out items with 0 quantity
        # Also need to handle rounding errors? Pydantic floats.
        # Let's assume strict checks for now.
        return [item for item in inventory.values() if item.quantity.value > 0]
