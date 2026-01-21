from enum import Enum
from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import Field, field_validator, ConfigDict

from .base import SystemContract

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
    PACKET = "PACKET"

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
        if self.unit == Unit.KILOGRAM:
            return Quantity(value=self.value * 1000, unit=Unit.GRAM, approx=self.approx)
        elif self.unit == Unit.LITER:
            return Quantity(value=self.value * 1000, unit=Unit.MILLILITER, approx=self.approx)
        return self

    def __add__(self, other: 'Quantity') -> 'Quantity':
        if self.unit != other.unit:
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
        return (
            self.name == other.name and
            self.variant == other.variant and
            self.brand == other.brand
        )

    def __hash__(self):
        return hash((self.name, self.variant, self.brand))

class InventoryItem(SystemContract):
    """
    D0.1 Inventory State Contract
    Represents the current state of an item in the inventory.
    """
    item: ItemIdentity
    quantity: Quantity
    expiry_date: Optional[date] = None
    status: StockStatus = StockStatus.IN_STOCK

    def is_in_stock(self) -> bool:
        """
        D0.1 'In Stock' Predicate:
        Quantity > 0 AND NOT expired (if expiry known).
        """
        if self.quantity.value <= 0:
            return False
        if self.expiry_date and self.expiry_date < date.today():
            return False
        return True

class InventoryState(SystemContract):
    """
    D0.1 Inventory State Contract
    Represents the full state of the inventory at a point in time.
    """
    items: List[InventoryItem] = Field(default_factory=list)

    def get_stock_snapshot(self) -> List[InventoryItem]:
        return [item for item in self.items if item.is_in_stock()]
