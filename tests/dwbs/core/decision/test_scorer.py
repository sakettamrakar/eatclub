import unittest
from unittest.mock import Mock, MagicMock
from datetime import date
from dwbs.core.decision.scoring.scorer import RecipeScorer
from dwbs.core.recipe.domain.recipe import Recipe
from dwbs.core.contracts.inventory import InventoryState, InventoryItem, ItemIdentity, StockStatus
from dwbs.core.recipe.domain.feasibility import FeasibilityChecker
from dwbs.core.recipe.domain.ingredient import IngredientRef

class TestRecipeScorer(unittest.TestCase):
    def setUp(self):
        self.mock_feasibility_checker = Mock(spec=FeasibilityChecker)
        self.mock_feasibility_checker.substitution_graph = None # Default no graph
        self.scorer = RecipeScorer(self.mock_feasibility_checker)

    def create_item_identity(self, name, confidence=1.0):
        # We need to ensure __str__ or attributes are accessed correctly in _get_key
        m = MagicMock()
        m.name = name
        m.variant = None
        m.brand = None
        m.confidence = confidence
        return m

    def create_inventory_item(self, item_identity, expiry_date=None, is_in_stock=True):
        m = MagicMock(spec=InventoryItem)
        m.item = item_identity
        m.expiry_date = expiry_date
        m.is_in_stock.return_value = is_in_stock
        return m

    def test_score_feasible_high_confidence(self):
        # Setup
        self.mock_feasibility_checker.can_cook.return_value = True

        # Recipe
        item_id = self.create_item_identity("Tomato")
        ingredient = MagicMock(spec=IngredientRef)
        ingredient.item = item_id

        recipe = MagicMock(spec=Recipe)
        recipe.ingredients = [ingredient]

        # Inventory
        inv_item = self.create_inventory_item(item_id)

        inventory = MagicMock(spec=InventoryState)
        inventory.items = [inv_item]

        # Execute
        score = self.scorer.score(recipe, inventory)

        # Assert
        self.assertEqual(score, 1.0)

    def test_score_feasible_low_confidence(self):
        # Setup
        self.mock_feasibility_checker.can_cook.return_value = True

        # Recipe
        item_id = self.create_item_identity("Tomato")
        ingredient = MagicMock(spec=IngredientRef)
        ingredient.item = item_id

        recipe = MagicMock(spec=Recipe)
        recipe.ingredients = [ingredient]

        # Inventory
        inv_item = self.create_inventory_item(self.create_item_identity("Tomato", confidence=0.4))

        inventory = MagicMock(spec=InventoryState)
        inventory.items = [inv_item]

        # Execute
        score = self.scorer.score(recipe, inventory)

        # Assert
        self.assertEqual(score, 0.4)

    def test_score_mixed_confidence(self):
        # Recipe needs Tomato and Onion
        # Tomato has conf 1.0, Onion has conf 0.4

        self.mock_feasibility_checker.can_cook.return_value = True

        t_id = self.create_item_identity("Tomato")
        o_id = self.create_item_identity("Onion")

        ing1 = MagicMock(spec=IngredientRef)
        ing1.item = t_id
        ing2 = MagicMock(spec=IngredientRef)
        ing2.item = o_id

        recipe = MagicMock(spec=Recipe)
        recipe.ingredients = [ing1, ing2]

        inv_t = self.create_inventory_item(self.create_item_identity("Tomato", confidence=1.0))
        inv_o = self.create_inventory_item(self.create_item_identity("Onion", confidence=0.4))

        inventory = MagicMock(spec=InventoryState)
        inventory.items = [inv_t, inv_o]

        score = self.scorer.score(recipe, inventory)
        self.assertEqual(score, 0.4)

    def test_score_multiple_items_max_confidence(self):
        # Recipe needs Tomato. Inventory has Tomato(0.4) and Tomato(0.9).
        # Should pick 0.9.

        self.mock_feasibility_checker.can_cook.return_value = True

        t_id = self.create_item_identity("Tomato")
        ing1 = MagicMock(spec=IngredientRef)
        ing1.item = t_id

        recipe = MagicMock(spec=Recipe)
        recipe.ingredients = [ing1]

        inv_t1 = self.create_inventory_item(self.create_item_identity("Tomato", confidence=0.4))
        inv_t2 = self.create_inventory_item(self.create_item_identity("Tomato", confidence=0.9))

        inventory = MagicMock(spec=InventoryState)
        inventory.items = [inv_t1, inv_t2]

        score = self.scorer.score(recipe, inventory)
        self.assertEqual(score, 0.9)

    def test_score_expiry_boost(self):
        # Recipe with expiring ingredient (confidence 1.0)
        # Should get 1.0 + 1.0 = 2.0

        self.mock_feasibility_checker.can_cook.return_value = True

        t_id = self.create_item_identity("Tomato")
        ing1 = MagicMock(spec=IngredientRef)
        ing1.item = t_id

        recipe = MagicMock(spec=Recipe)
        recipe.ingredients = [ing1]

        today = date(2025, 1, 1)
        expiring_date = date(2025, 1, 2) # Today + 1 day

        inv_item = self.create_inventory_item(t_id, expiry_date=expiring_date)

        inventory = MagicMock(spec=InventoryState)
        inventory.items = [inv_item]

        score = self.scorer.score(recipe, inventory, today=today)
        self.assertEqual(score, 2.0)

    def test_score_no_expiry_boost(self):
        # Recipe with ingredient expiring later (confidence 1.0)
        # Should get 1.0

        self.mock_feasibility_checker.can_cook.return_value = True

        t_id = self.create_item_identity("Tomato")
        ing1 = MagicMock(spec=IngredientRef)
        ing1.item = t_id

        recipe = MagicMock(spec=Recipe)
        recipe.ingredients = [ing1]

        today = date(2025, 1, 1)
        future_date = date(2025, 1, 5) # Today + 4 days

        inv_item = self.create_inventory_item(t_id, expiry_date=future_date)

        inventory = MagicMock(spec=InventoryState)
        inventory.items = [inv_item]

        score = self.scorer.score(recipe, inventory, today=today)
        self.assertEqual(score, 1.0)

    def test_score_expiry_boost_low_confidence(self):
        # Recipe with expiring ingredient (confidence 0.4)
        # Should get 0.4 + 1.0 = 1.4

        self.mock_feasibility_checker.can_cook.return_value = True

        t_id = self.create_item_identity("Tomato", confidence=0.4)
        ing1 = MagicMock(spec=IngredientRef)
        ing1.item = t_id

        recipe = MagicMock(spec=Recipe)
        recipe.ingredients = [ing1]

        today = date(2025, 1, 1)
        expiring_date = date(2025, 1, 2)

        inv_item = self.create_inventory_item(t_id, expiry_date=expiring_date)

        inventory = MagicMock(spec=InventoryState)
        inventory.items = [inv_item]

        score = self.scorer.score(recipe, inventory, today=today)
        self.assertEqual(score, 1.4)

if __name__ == '__main__':
    unittest.main()
