import unittest
from unittest.mock import Mock, MagicMock
from dwbs.core.decision.logic.recommender import ActionRecommender, SuggestRecipeAction, AskUserAction, NoAction
from dwbs.core.decision.scoring.scorer import RecipeScorer
from dwbs.core.decision.explanation.generator import ExplanationGenerator
from dwbs.core.recipe.domain.recipe import Recipe
from dwbs.core.contracts.inventory import InventoryState
from dwbs.core.contracts.explanation import Explanation

class TestActionRecommender(unittest.TestCase):
    def setUp(self):
        self.mock_scorer = Mock(spec=RecipeScorer)
        self.mock_explanation_generator = Mock(spec=ExplanationGenerator)
        self.recommender = ActionRecommender(self.mock_scorer, self.mock_explanation_generator)

        # Default mock explanation
        self.mock_explanation = Explanation(reason="Test", source_fact="Test", confidence=1.0)
        self.mock_explanation_generator.generate_suggestion_explanation.return_value = self.mock_explanation
        self.mock_explanation_generator.generate_ask_user_explanation.return_value = self.mock_explanation

    def test_recommend_high_confidence(self):
        # Setup
        r1 = MagicMock(spec=Recipe)
        r1.name = "R1"
        inventory = MagicMock(spec=InventoryState)

        self.mock_scorer.score.return_value = 1.0

        # Execute
        action = self.recommender.recommend([r1], inventory)

        # Assert
        self.assertIsInstance(action, SuggestRecipeAction)
        self.assertEqual(action.recipe, r1)
        self.assertEqual(action.score, 1.0)
        self.assertEqual(action.explanation, self.mock_explanation)

    def test_recommend_low_confidence(self):
        # Setup
        r1 = MagicMock(spec=Recipe)
        r1.name = "R1"
        inventory = MagicMock(spec=InventoryState)

        self.mock_scorer.score.return_value = 0.4

        # Execute
        action = self.recommender.recommend([r1], inventory)

        # Assert
        self.assertIsInstance(action, AskUserAction)
        self.assertEqual(action.target_recipe, r1)
        self.assertTrue("R1" in action.question)
        self.assertEqual(action.explanation, self.mock_explanation)

    def test_recommend_none_feasible(self):
        # Setup
        r1 = MagicMock(spec=Recipe)
        inventory = MagicMock(spec=InventoryState)

        self.mock_scorer.score.return_value = 0.0

        # Execute
        action = self.recommender.recommend([r1], inventory)

        # Assert
        self.assertIsInstance(action, NoAction)

    def test_recommend_sorting(self):
        # Setup
        r1 = MagicMock(spec=Recipe)
        r1.name = "R1"
        r2 = MagicMock(spec=Recipe)
        r2.name = "R2"
        inventory = MagicMock(spec=InventoryState)

        # R1 score 0.8, R2 score 0.9
        self.mock_scorer.score.side_effect = lambda r, i, today=None: 0.8 if r == r1 else 0.9

        # Execute
        action = self.recommender.recommend([r1, r2], inventory)

        # Assert
        self.assertIsInstance(action, SuggestRecipeAction)
        self.assertEqual(action.recipe, r2)
        self.assertEqual(action.score, 0.9)

if __name__ == '__main__':
    unittest.main()
