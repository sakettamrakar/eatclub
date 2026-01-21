from typing import Optional
from datetime import date, timedelta
from ...contracts.explanation import Explanation
from ...recipe.domain.recipe import Recipe
from ...contracts.inventory import InventoryState
from ..scoring.scorer import RecipeScorer

class ExplanationGenerator:
    """
    D3.5 Explanation Generator
    Deterministically generates human-readable explanations.
    """
    def __init__(self, scorer: RecipeScorer):
        self.scorer = scorer

    def generate_suggestion_explanation(self, recipe: Recipe, inventory: InventoryState, score: float, today: Optional[date] = None) -> Explanation:
        if today is None:
            today = date.today()

        # Check for expiry first (Highest Priority for explanation)
        inventory_map = self.scorer.build_inventory_map(inventory)
        expiry_threshold = today + timedelta(days=2)

        earliest_expiry_item = None
        earliest_expiry_date = None

        for ingredient in recipe.ingredients:
            candidates = self.scorer.get_candidates(ingredient, inventory_map)
            for cand in candidates:
                if cand.expiry_date and cand.expiry_date < expiry_threshold:
                    if earliest_expiry_date is None or cand.expiry_date < earliest_expiry_date:
                        earliest_expiry_date = cand.expiry_date
                        earliest_expiry_item = cand

        if earliest_expiry_item:
            days = (earliest_expiry_date - today).days
            if days <= 0:
                time_str = "today"
            elif days == 1:
                time_str = "tomorrow"
            else:
                time_str = f"in {days} days"

            return Explanation(
                reason=f"Recommended because {earliest_expiry_item.item.name} expires {time_str}.",
                source_fact="rule:expiry_prioritization",
                confidence=1.0
            )

        # Confidence based explanation
        if score >= 0.9:
            return Explanation(
                reason="Excellent match with high confidence inventory.",
                source_fact="rule:high_confidence",
                confidence=1.0
            )
        elif score >= 0.6:
            return Explanation(
                reason="Good match.",
                source_fact="rule:medium_confidence",
                confidence=1.0
            )
        else:
            return Explanation(
                 reason="Low confidence match.",
                 source_fact="rule:low_confidence",
                 confidence=1.0
            )

    def generate_ask_user_explanation(self, recipe: Recipe, score: float) -> Explanation:
        return Explanation(
            reason=f"Confidence score {score:.1f} is too low.",
            source_fact="rule:confidence_threshold",
            confidence=1.0
        )
