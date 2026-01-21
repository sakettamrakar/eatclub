from typing import Optional
from pydantic import Field
from ..contracts import SystemContract

class ItemIdentity(SystemContract):
    """
    D1.2 Item Identity Resolution
    Distinguish specific forms of ingredients.
    Strict identity means name, variant, and brand must match exactly if present.
    """
    name: str = Field(..., min_length=1, description="Canonical name of the item (e.g. 'Tomato')")
    variant: Optional[str] = Field(None, description="Form or processing state (e.g. 'Canned', 'Puree', 'Chopped')")
    brand: Optional[str] = Field(None, description="Brand name if relevant")

    # Keeping confidence as float for now until Task 2.5
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Confidence in this identity (Source reliability)")

    def full_name(self) -> str:
        parts = [self.name]
        if self.variant:
            parts.append(f"({self.variant})")
        if self.brand:
            parts.append(f"[{self.brand}]")
        return " ".join(parts)

    def __eq__(self, other):
        if not isinstance(other, ItemIdentity):
            return False
        # Strict equality on fields (Pydantic models usually handle this, but strictness is emphasized)
        # Case sensitivity? "Tomato" vs "tomato".
        # Task says "Strict ID equivalence". Usually implies case sensitive unless specified otherwise.
        # "Distinguish Tomato (Fresh) vs Tomato (Canned)".
        return (
            self.name == other.name and
            self.variant == other.variant and
            self.brand == other.brand
        )

    def __hash__(self):
        return hash((self.name, self.variant, self.brand))
