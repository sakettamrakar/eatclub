from typing import List, Union, Optional, Tuple
from pydantic import Field
from ...contracts.base import SystemContract
from ...contracts.explanation import Explanation
from ...recipe.domain.recipe import Recipe
from ...contracts.inventory import InventoryState
from ..scoring.scorer import RecipeScorer
from ..explanation.generator import ExplanationGenerator

class Action(SystemContract):
    explanation: Explanation

class SuggestRecipeAction(Action):
    recipe: Recipe
    score: float

class AskUserAction(Action):
    question: str
    target_recipe: Optional[Recipe] = None

class NoAction(Action):
    pass

class ActionRecommender:
    """
    D3.4 "Ask User" Branch
    Decides whether to suggest a recipe or ask for clarification.
    """
    def __init__(self, scorer: RecipeScorer, explanation_generator: ExplanationGenerator):
        self.scorer = scorer
        self.explanation_generator = explanation_generator
        self.confidence_threshold = 0.6

    def recommend(self, recipes: List[Recipe], inventory: InventoryState) -> Action:
        scored_recipes: List[Tuple[Recipe, float]] = []
        for r in recipes:
            score = self.scorer.score(r, inventory)
            if score > 0:
                scored_recipes.append((r, score))

        if not scored_recipes:
            return NoAction(
                explanation=Explanation(
                    reason="No feasible recipes found.",
                    source_fact="rule:feasibility",
                    confidence=1.0
                )
            )

        # Sort desc
        scored_recipes.sort(key=lambda x: x[1], reverse=True)

        top_recipe, top_score = scored_recipes[0]

        if top_score < self.confidence_threshold:
            # Low confidence
            explanation = self.explanation_generator.generate_ask_user_explanation(top_recipe, top_score)
            return AskUserAction(
                explanation=explanation,
                question=f"Do you have the ingredients for {top_recipe.name}?",
                target_recipe=top_recipe
            )
        else:
            explanation = self.explanation_generator.generate_suggestion_explanation(top_recipe, inventory, top_score)
            return SuggestRecipeAction(
                explanation=explanation,
                recipe=top_recipe,
                score=top_score
            )
