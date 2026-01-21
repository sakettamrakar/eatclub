from typing import Optional, List, Dict
from datetime import date, timedelta
from ...recipe.domain.recipe import Recipe
from ...contracts.inventory import InventoryState, InventoryItem
from ...recipe.domain.feasibility import FeasibilityChecker

class RecipeScorer:
    """
    D3.1 Feasibility Scoring
    Scoring engine for recipes.
    """

    EXPIRY_BOOST = 1.0

    def __init__(self, feasibility_checker: FeasibilityChecker):
        self.feasibility_checker = feasibility_checker

    def score(self, recipe: Recipe, inventory_state: InventoryState, today: Optional[date] = None) -> float:
        """
        Calculates the score for a recipe given the current inventory state.
        Base implementation: Returns 1.0 if feasible, 0.0 otherwise.
        Refined (Task 4.2): Multiply score by lowest ingredient confidence.
        Refined (Task 4.3): Add boost if any ingredient is expiring (< today + 2 days).
        """
        if not self.feasibility_checker.can_cook(recipe, inventory_state):
            return 0.0

        if today is None:
            today = date.today()

        min_ingredient_confidence = 1.0
        has_expiring_ingredient = False
        expiry_threshold = today + timedelta(days=2)

        inventory_map = self.build_inventory_map(inventory_state)

        for ingredient in recipe.ingredients:
            candidates = self.get_candidates(ingredient, inventory_map)

            if not candidates:
                # Should not happen if can_cook is True
                return 0.0

            # Optimistic: use best confidence available for this ingredient
            best_conf = max(c.item.confidence for c in candidates)
            min_ingredient_confidence = min(min_ingredient_confidence, best_conf)

            # Check for expiring items
            if not has_expiring_ingredient:
                for cand in candidates:
                    if cand.expiry_date and cand.expiry_date < expiry_threshold:
                        has_expiring_ingredient = True
                        break

        final_score = min_ingredient_confidence + (self.EXPIRY_BOOST if has_expiring_ingredient else 0.0)
        return final_score

    def build_inventory_map(self, inventory_state: InventoryState) -> Dict[str, List[InventoryItem]]:
        inventory_map: Dict[str, List[InventoryItem]] = {}
        for item in inventory_state.items:
            if item.is_in_stock():
                key = self.get_key(item.item)
                if key not in inventory_map:
                    inventory_map[key] = []
                inventory_map[key].append(item)
        return inventory_map

    def get_candidates(self, ingredient, inventory_map: Dict[str, List[InventoryItem]]) -> List[InventoryItem]:
        candidates: List[InventoryItem] = []
        # Direct
        key = self.get_key(ingredient.item)
        if key in inventory_map:
            candidates.extend(inventory_map[key])

        # Substitutes
        if self.feasibility_checker.substitution_graph:
            substitutes = self.feasibility_checker.substitution_graph.get_substitutes(ingredient.item)
            for sub_item, _ in substitutes:
                sub_key = self.get_key(sub_item)
                if sub_key in inventory_map:
                    candidates.extend(inventory_map[sub_key])
        return candidates

    def get_key(self, item_identity) -> str:
        # Match FeasibilityChecker logic
        return f"{item_identity.name}|{item_identity.variant}|{item_identity.brand}"
