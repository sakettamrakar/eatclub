from uuid import UUID, uuid4
from datetime import datetime, date
from typing import Optional, Union, Literal
from pydantic import Field, ConfigDict

from ...contracts import SystemContract, MutationType, MutationSource, Explanation
from ...contracts.inventory import ItemIdentity, Quantity
from ..waste.reasons import WasteReason

class BasePayload(SystemContract):
    """Base class for event payloads."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

class PurchasePayload(BasePayload):
    item: ItemIdentity
    quantity: Quantity
    expiry_date: Optional[date] = None
    source: MutationSource
    explanation: Explanation

class ConsumePayload(BasePayload):
    item: ItemIdentity
    quantity: Quantity
    source: MutationSource
    explanation: Explanation

class WastePayload(BasePayload):
    item: ItemIdentity
    quantity: Quantity
    reason: WasteReason
    source: MutationSource
    explanation: Explanation

class CorrectionPayload(BasePayload):
    item: ItemIdentity
    quantity_delta: Quantity
    source: MutationSource
    explanation: Explanation

class LedgerEvent(SystemContract):
    """
    D1.1 Event-Sourcing Lite
    Immutable record of a change to the inventory.
    """
    event_id: UUID = Field(default_factory=uuid4, description="Unique event ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the event occurred")
    actor: str = Field(..., description="The entity performing the action")
    mutation_type: MutationType = Field(..., description="Type of operation")
    expected_version: Optional[int] = Field(None, description="Optimistic locking: required version for this event to be valid.")

class PurchaseEvent(LedgerEvent):
    mutation_type: Literal[MutationType.PURCHASE] = MutationType.PURCHASE
    payload: PurchasePayload

class ConsumeEvent(LedgerEvent):
    mutation_type: Literal[MutationType.CONSUME] = MutationType.CONSUME
    payload: ConsumePayload

class WasteEvent(LedgerEvent):
    mutation_type: Literal[MutationType.WASTE] = MutationType.WASTE
    payload: WastePayload

class CorrectionAddEvent(LedgerEvent):
    mutation_type: Literal[MutationType.CORRECTION_ADD] = MutationType.CORRECTION_ADD
    payload: CorrectionPayload

class CorrectionRemoveEvent(LedgerEvent):
    mutation_type: Literal[MutationType.CORRECTION_REMOVE] = MutationType.CORRECTION_REMOVE
    payload: CorrectionPayload

InventoryEvent = Union[
    PurchaseEvent,
    ConsumeEvent,
    WasteEvent,
    CorrectionAddEvent,
    CorrectionRemoveEvent
]
