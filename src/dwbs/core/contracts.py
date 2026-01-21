from enum import Enum, auto
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class StockStatus(str, Enum):
    """
    D0.1 Inventory State Contract
    Strict definition of stock status.
    """
    IN_STOCK = "IN_STOCK"
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"

class MutationSource(str, Enum):
    """
    D0.2 Mutation Rules
    Defines who/what is authorizing the change.
    """
    USER_MANUAL = "USER_MANUAL"  # Explicit user action
    USER_CONFIRMED_OCR = "USER_CONFIRMED_OCR"  # User approved OCR draft
    SYSTEM_LOGIC = "SYSTEM_LOGIC"  # Deterministic system logic (e.g. expiry update)
    # Note: ML/LLM sources would be lower trust and are not core sources for truth mutations

class MutationType(str, Enum):
    """
    D0.2 Mutation Rules
    Defines the type of operation on the ledger.
    """
    PURCHASE = "PURCHASE"      # Adding new stock
    CONSUME = "CONSUME"        # Cooking/Eating
    WASTE = "WASTE"            # Throwing away
    CORRECTION_ADD = "CORRECTION_ADD"      # Finding untracked items
    CORRECTION_REMOVE = "CORRECTION_REMOVE" # Removing items that were tracked erroneously
    SNAPSHOT = "SNAPSHOT"      # Periodic reconciliation (if needed)

class Explanation(BaseModel):
    """
    D0.3 Explainability Contract
    Every system suggestion or major state change must have a rationale.
    """
    model_config = ConfigDict(frozen=True)

    summary: str = Field(..., description="Short human-readable summary of the reason.")
    details: Optional[str] = Field(None, description="Detailed explanation.")
    source_rule: str = Field(..., description="ID of the rule or logic that generated this.")
    confidence_score: float = Field(1.0, ge=0.0, le=1.0, description="Confidence in this explanation.")

class SystemContract(BaseModel):
    """Base class for all system contracts to ensure runtime validation."""
    model_config = ConfigDict(frozen=True)
