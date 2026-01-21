import unittest
from unittest.mock import Mock, MagicMock
from dwbs.core.decision.logic.recommender import ActionRecommender, SuggestRecipeAction
from dwbs.core.decision.scoring.scorer import RecipeScorer
from dwbs.core.decision.explanation.generator import ExplanationGenerator
from dwbs.core.recipe.domain.recipe import Recipe
from dwbs.core.contracts.inventory import InventoryState, InventoryItem
from dwbs.core.recipe.domain.feasibility import FeasibilityChecker
from dwbs.core.recipe.domain.ingredient import IngredientRef

class TestDecisionDeterminism(unittest.TestCase):
    def test_determinism(self):
        # Setup Component Chain
        feasibility_checker = Mock(spec=FeasibilityChecker)
        feasibility_checker.can_cook.return_value = True
        feasibility_checker.substitution_graph = None

        scorer = RecipeScorer(feasibility_checker)
        explanation_generator = ExplanationGenerator(scorer)
        recommender = ActionRecommender(scorer, explanation_generator)

        # Data
        item_id = MagicMock()
        item_id.name = "Tomato"
        item_id.confidence = 1.0
        # Mock __str__ if needed by get_key, or just set name/variant/brand
        item_id.variant = None
        item_id.brand = None

        ingredient = MagicMock(spec=IngredientRef)
        ingredient.item = item_id

        recipe = MagicMock(spec=Recipe)
        recipe.ingredients = [ingredient]
        recipe.name = "Tomato Soup"

        inv_item = MagicMock(spec=InventoryItem)
        inv_item.item = item_id
        inv_item.expiry_date = None
        inv_item.is_in_stock.return_value = True

        inventory = MagicMock(spec=InventoryState)
        inventory.items = [inv_item]

        # Run 1
        action1 = recommender.recommend([recipe], inventory)

        # Run 2
        action2 = recommender.recommend([recipe], inventory)

        # Assertions
        # 1. Output type identity
        self.assertIsInstance(action1, SuggestRecipeAction)
        self.assertIsInstance(action2, SuggestRecipeAction)

        # 2. Score equality
        self.assertEqual(action1.score, action2.score)

        # 3. Explanation equality
        self.assertEqual(action1.explanation.reason, action2.explanation.reason)
        self.assertEqual(action1.explanation.source_fact, action2.explanation.source_fact)

        # 4. Object equality (if implemented) or field equality
        # Since they are pydantic models, __eq__ works on fields
        self.assertEqual(action1, action2)

if __name__ == '__main__':
    unittest.main()
