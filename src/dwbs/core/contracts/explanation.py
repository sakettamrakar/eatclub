from typing import Optional
from pydantic import Field
from .base import SystemContract

class Explanation(SystemContract):
    """
    D0.3 Explainability Contract
    Every system suggestion or major state change must have a rationale.
    """
    reason: str = Field(..., description="Short human-readable summary of the reason.")
    source_fact: str = Field(..., description="ID of the rule or logic that generated this.")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Confidence in this explanation.")
    details: Optional[str] = Field(None, description="Detailed explanation.")
