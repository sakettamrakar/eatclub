from typing import Dict, List, Optional
from ...contracts.inventory import InventoryState, ItemIdentity, Quantity
from .recipe import Recipe
from ..graph.substitution import SubstitutionGraph

class FeasibilityChecker:
    """
    D2 Recipe Knowledge Graph
    Logic to check if a recipe can be cooked given the current inventory.
    """

    def __init__(self, substitution_graph: Optional[SubstitutionGraph] = None):
        self.substitution_graph = substitution_graph

    def can_cook(self, recipe: Recipe, inventory: InventoryState) -> bool:
        """
        Returns True if all ingredients are present in sufficient quantity,
        considering substitutions if a graph is provided.
        """
        # 1. Aggregate inventory stock
        # Map: ItemIdentity -> Total Quantity
        # Note: We need to handle units. We'll normalize everything to base units if possible,
        # but Quantity contract only normalizes within same type (Weight/Volume).
        # We'll assume strict unit matching or normalization for now.

        stock: Dict[str, Quantity] = {} # Keyed by full_name or hash of Identity

        # Helper to key
        def get_key(item_id: ItemIdentity) -> str:
            # We use full_name as key for aggregation since ItemIdentity is value object
            # But wait, ItemIdentity might differ in confidence.
            # We strictly match name, variant, brand.
            return f"{item_id.name}|{item_id.variant}|{item_id.brand}"

        # We also need a way to store the Identity object for substitution lookups
        item_map: Dict[str, ItemIdentity] = {}

        for inv_item in inventory.items:
            if not inv_item.is_in_stock():
                continue

            key = get_key(inv_item.item)
            item_map[key] = inv_item.item

            if key not in stock:
                stock[key] = inv_item.quantity
            else:
                try:
                    stock[key] = stock[key] + inv_item.quantity
                except ValueError:
                    # Mixed units (e.g. Grams vs Pieces) for same item?
                    # Should not happen in well-formed inventory, but if it does, we keep separate?
                    # For Phase 1, we assume consistent units for same item.
                    pass

        # 2. Check each ingredient
        for ingredient in recipe.ingredients:
            required_qty = ingredient.quantity
            required_item = ingredient.item
            required_key = get_key(required_item)

            # Check if we have enough of the exact item
            if self._has_sufficient_quantity(stock.get(required_key), required_qty):
                continue

            # Not enough exact item. Check substitutions.
            if self.substitution_graph:
                substitutes = self.substitution_graph.get_substitutes(required_item)
                found_substitute = False
                for sub_item, penalty in substitutes:
                    sub_key = get_key(sub_item)
                    if self._has_sufficient_quantity(stock.get(sub_key), required_qty):
                        found_substitute = True
                        break

                if found_substitute:
                    continue

            # Missing ingredient
            return False

        return True

    def _has_sufficient_quantity(self, available: Optional[Quantity], required: Quantity) -> bool:
        if not available:
            return False

        # Try to compare. normalize() handles unit conversion (kg->g).
        try:
             # We use < operator from Quantity which handles normalization
             if available < required:
                 return False
             return True
        except ValueError:
            # Incompatible units (e.g. L vs Kg)
            return False
