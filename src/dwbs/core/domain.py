from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from .contracts import SystemContract

class Unit(str, Enum):
    """
    D1.3 Quantity & Unit Normalization
    Standardized units for inventory.
    """
    # Weight
    GRAM = "G"
    KILOGRAM = "KG"

    # Volume
    MILLILITER = "ML"
    LITER = "L"

    # Count
    PIECE = "PCS"

    # Imprecise (to be used with caution/heuristics later)
    BUNCH = "BUNCH"
    PINCH = "PINCH"
    PACKET = "PACKET" # Requires metadata for normalization

class Quantity(SystemContract):
    """
    D1.3 Quantity & Unit Normalization
    Represents a physical quantity with a unit.
    """
    value: float = Field(..., ge=0, description="The numerical amount. Must be non-negative.")
    unit: Unit = Field(..., description="The unit of measurement.")

    @field_validator('value')
    def value_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Quantity value must be non-negative')
        return v

    def normalize(self) -> 'Quantity':
        """
        Returns a normalized version of the quantity (e.g., KG -> G, L -> ML).
        """
        if self.unit == Unit.KILOGRAM:
            return Quantity(value=self.value * 1000, unit=Unit.GRAM)
        elif self.unit == Unit.LITER:
            return Quantity(value=self.value * 1000, unit=Unit.MILLILITER)
        return self

    def __add__(self, other: 'Quantity') -> 'Quantity':
        if self.unit != other.unit:
             # Simple conversion attempt for common cases
            norm_self = self.normalize()
            norm_other = other.normalize()
            if norm_self.unit == norm_other.unit:
                return Quantity(value=norm_self.value + norm_other.value, unit=norm_self.unit)
            raise ValueError(f"Cannot add different units: {self.unit} and {other.unit}")
        return Quantity(value=self.value + other.value, unit=self.unit)

    def __sub__(self, other: 'Quantity') -> 'Quantity':
        if self.unit != other.unit:
             # Simple conversion attempt
            norm_self = self.normalize()
            norm_other = other.normalize()
            if norm_self.unit == norm_other.unit:
                return Quantity(value=norm_self.value - norm_other.value, unit=norm_self.unit)
            raise ValueError(f"Cannot subtract different units: {self.unit} and {other.unit}")
        return Quantity(value=self.value - other.value, unit=self.unit)

    def __lt__(self, other: 'Quantity') -> bool:
         # Normalize for comparison
        norm_self = self.normalize()
        norm_other = other.normalize()
        if norm_self.unit != norm_other.unit:
             raise ValueError(f"Cannot compare different units: {self.unit} and {other.unit}")
        return norm_self.value < norm_other.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        norm_self = self.normalize()
        norm_other = other.normalize()
        return norm_self.value == norm_other.value and norm_self.unit == norm_other.unit

class ItemIdentity(SystemContract):
    """
    D1.2 Item Identity Resolution
    Distinguish specific forms of ingredients.
    """
    name: str = Field(..., min_length=1, description="Canonical name of the item (e.g. 'Tomato')")
    variant: Optional[str] = Field(None, description="Form or processing state (e.g. 'Canned', 'Puree', 'Chopped')")
    brand: Optional[str] = Field(None, description="Brand name if relevant")

    # D1.4 Confidence Scores (Default 1.0 for manual entry)
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Confidence in this identity (Source reliability)")

    def full_name(self) -> str:
        parts = [self.name]
        if self.variant:
            parts.append(f"({self.variant})")
        if self.brand:
            parts.append(f"[{self.brand}]")
        return " ".join(parts)
