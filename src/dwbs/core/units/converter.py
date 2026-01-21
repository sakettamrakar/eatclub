from enum import Enum
from decimal import Decimal
from typing import Optional
from pydantic import Field, field_validator
from ..contracts import SystemContract

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
    Uses Decimal for precision.
    """
    value: Decimal = Field(..., description="The numerical amount. Must be non-negative.")
    unit: Unit = Field(..., description="The unit of measurement.")
    approx: bool = Field(False, description="Whether this quantity is an approximation.")

    @field_validator('value')
    def value_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Quantity value must be non-negative')
        return v

    def normalize(self) -> 'Quantity':
        """
        Returns a normalized version of the quantity (e.g., KG -> G, L -> ML).
        """
        # We normalize to base units: G, ML, PCS
        if self.unit == Unit.KILOGRAM:
            return Quantity(value=self.value * 1000, unit=Unit.GRAM, approx=self.approx)
        elif self.unit == Unit.LITER:
            return Quantity(value=self.value * 1000, unit=Unit.MILLILITER, approx=self.approx)
        return self

    def __add__(self, other: 'Quantity') -> 'Quantity':
        if self.unit != other.unit:
             # Simple conversion attempt for common cases
            norm_self = self.normalize()
            norm_other = other.normalize()
            if norm_self.unit == norm_other.unit:
                return Quantity(
                    value=norm_self.value + norm_other.value,
                    unit=norm_self.unit,
                    approx=self.approx or other.approx
                )
            raise ValueError(f"Cannot add different units: {self.unit} and {other.unit}")
        return Quantity(
            value=self.value + other.value,
            unit=self.unit,
            approx=self.approx or other.approx
        )

    def __sub__(self, other: 'Quantity') -> 'Quantity':
        if self.unit != other.unit:
             # Simple conversion attempt
            norm_self = self.normalize()
            norm_other = other.normalize()
            if norm_self.unit == norm_other.unit:
                return Quantity(
                    value=norm_self.value - norm_other.value,
                    unit=norm_self.unit,
                    approx=self.approx or other.approx
                )
            raise ValueError(f"Cannot subtract different units: {self.unit} and {other.unit}")
        return Quantity(
            value=self.value - other.value,
            unit=self.unit,
            approx=self.approx or other.approx
        )

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
        # Decimal comparison handles floating point issues
        return norm_self.value == norm_other.value and norm_self.unit == norm_other.unit
