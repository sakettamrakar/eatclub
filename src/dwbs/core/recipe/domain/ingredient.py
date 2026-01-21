from pydantic import Field
from ...contracts.base import SystemContract
from ...contracts.inventory import ItemIdentity, Quantity

class IngredientRef(SystemContract):
    """
    D2.1 Structured Ingredient Mappings
    Reference to an ingredient required by a recipe.
    """
    item: ItemIdentity = Field(..., description="The identity of the required item.")
    quantity: Quantity = Field(..., description="The required quantity.")
    notes: str = Field("", description="Optional notes for preparation (e.g. 'finely chopped')")

    def __str__(self) -> str:
        return f"{self.quantity.value}{self.quantity.unit.value} {self.item.full_name()}"
