from enum import Enum
from typing import Protocol, TYPE_CHECKING
from pydantic import Field, ConfigDict
from .base import SystemContract

if TYPE_CHECKING:
    from .inventory import InventoryState

class MutationSource(str, Enum):
    """
    D0.2 Mutation Rules
    Defines who/what is authorizing the change.
    """
    USER_MANUAL = "USER_MANUAL"
    USER_CONFIRMED_OCR = "USER_CONFIRMED_OCR"
    SYSTEM_LOGIC = "SYSTEM_LOGIC"

class MutationType(str, Enum):
    """
    D0.2 Mutation Rules
    Defines the type of operation on the ledger.
    """
    PURCHASE = "PURCHASE"
    CONSUME = "CONSUME"
    WASTE = "WASTE"
    CORRECTION_ADD = "CORRECTION_ADD"
    CORRECTION_REMOVE = "CORRECTION_REMOVE"
    SNAPSHOT = "SNAPSHOT"

class InventoryMutation(SystemContract):
    """
    D0.2 Mutation Rules
    Base class for all inventory mutations.
    """
    mutation_type: MutationType
    source: MutationSource

class Bought(InventoryMutation):
    mutation_type: MutationType = MutationType.PURCHASE

class Consumed(InventoryMutation):
    mutation_type: MutationType = MutationType.CONSUME

class Wasted(InventoryMutation):
    mutation_type: MutationType = MutationType.WASTE
    reason: str = Field(..., description="Reason for waste (e.g. Expired, Spilled)")

class CorrectionAdd(InventoryMutation):
    mutation_type: MutationType = MutationType.CORRECTION_ADD

class CorrectionRemove(InventoryMutation):
    mutation_type: MutationType = MutationType.CORRECTION_REMOVE

class MutationVerifier(Protocol):
    """
    D0.2 Mutation Rules
    Interface for verifying if a mutation is valid given the current state.
    """
    def verify(self, mutation: InventoryMutation, current_state: 'InventoryState') -> bool:
        ...
