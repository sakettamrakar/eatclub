from typing import Dict
from ...contracts.inventory import ItemIdentity, Quantity, Unit

class YieldCalculator:
    """
    D2.2 Loss Factors
    Calculates yield (shrinkage/loss) from raw to cooked state.
    Formula: raw_qty * yield_factor = cooked_qty
    """

    # Hardcoded factors for Phase 1
    # Key: Item Name (canonical).
    # TODO: Move to a config or database later.
    _FACTORS: Dict[str, float] = {
        "Spinach": 0.6,
        "Mushroom": 0.5,
        "Onion": 0.8,
        "Rice": 3.0, # Expands!
        "Pasta": 2.5, # Expands!
    }

    def get_yield_factor(self, item_name: str) -> float:
        """
        Returns the yield factor for a given item name.
        Default is 1.0 (no change).
        """
        return self._FACTORS.get(item_name, 1.0)

    def calculate_cooked_quantity(self, item: ItemIdentity, raw_quantity: Quantity) -> Quantity:
        """
        Returns the expected cooked quantity given a raw quantity.
        """
        factor = self.get_yield_factor(item.name)
        new_value = raw_quantity.value * factor
        # Unit stays the same for now, assuming weight->weight or vol->vol
        # For Rice/Pasta, expansion usually implies weight increase (water absorption) or volume increase.
        return Quantity(value=new_value, unit=raw_quantity.unit)

    def calculate_raw_needed(self, item: ItemIdentity, target_cooked_quantity: Quantity) -> Quantity:
        """
        Returns the required raw quantity to achieve a target cooked quantity.
        """
        factor = self.get_yield_factor(item.name)
        if factor == 0:
            raise ValueError(f"Yield factor for {item.name} is 0, impossible to calculate raw needed.")

        new_value = target_cooked_quantity.value / factor
        return Quantity(value=new_value, unit=target_cooked_quantity.unit)
