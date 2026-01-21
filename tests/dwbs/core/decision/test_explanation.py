import unittest
from unittest.mock import Mock, MagicMock
from datetime import date
from dwbs.core.decision.explanation.generator import ExplanationGenerator
from dwbs.core.decision.scoring.scorer import RecipeScorer
from dwbs.core.recipe.domain.recipe import Recipe
from dwbs.core.contracts.inventory import InventoryState, InventoryItem
from dwbs.core.recipe.domain.ingredient import IngredientRef

class TestExplanationGenerator(unittest.TestCase):
    def setUp(self):
        self.mock_scorer = Mock(spec=RecipeScorer)
        self.generator = ExplanationGenerator(self.mock_scorer)

    def test_generate_suggestion_expiry(self):
        # Setup
        r1 = MagicMock(spec=Recipe)
        ingredient = MagicMock(spec=IngredientRef)
        r1.ingredients = [ingredient]

        inventory = MagicMock(spec=InventoryState)

        today = date(2025, 1, 1)
        expiry_date = date(2025, 1, 2) # Tomorrow

        inv_item = MagicMock(spec=InventoryItem)
        inv_item.expiry_date = expiry_date
        inv_item.item = MagicMock()
        inv_item.item.name = "Milk"

        # Scorer mock behavior
        self.mock_scorer.build_inventory_map.return_value = {}
        self.mock_scorer.get_candidates.return_value = [inv_item]

        # Execute
        explanation = self.generator.generate_suggestion_explanation(r1, inventory, 2.0, today=today)

        # Assert
        self.assertEqual(explanation.reason, "Recommended because Milk expires tomorrow.")
        self.assertEqual(explanation.source_fact, "rule:expiry_prioritization")

    def test_generate_suggestion_high_confidence(self):
        # Setup
        r1 = MagicMock(spec=Recipe)
        r1.ingredients = []
        inventory = MagicMock(spec=InventoryState)

        self.mock_scorer.build_inventory_map.return_value = {}
        # No expiring items

        # Execute
        explanation = self.generator.generate_suggestion_explanation(r1, inventory, 1.0)

        # Assert
        self.assertEqual(explanation.reason, "Excellent match with high confidence inventory.")

    def test_generate_ask_user(self):
        r1 = MagicMock(spec=Recipe)
        explanation = self.generator.generate_ask_user_explanation(r1, 0.4)
        self.assertEqual(explanation.reason, "Confidence score 0.4 is too low.")

if __name__ == '__main__':
    unittest.main()
