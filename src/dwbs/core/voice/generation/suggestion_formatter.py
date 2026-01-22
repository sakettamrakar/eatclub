from typing import List
from ...recipe.domain.recipe import Recipe

class SpokenSuggestionFormatter:
    """
    D9.3 Cooking suggestions
    """

    def format_suggestions(self, recipes: List[Recipe]) -> str:
        """
        Format top 3 recipes for speech.
        """
        if not recipes:
             return "I don't have any recipe suggestions right now."

        top_recipes = recipes[:3]
        recipe_names = [r.name for r in top_recipes]

        if len(recipe_names) == 1:
            return f"You could cook {recipe_names[0]}."
        elif len(recipe_names) == 2:
             return f"You could cook {recipe_names[0]} or {recipe_names[1]}."
        else:
            # Format: A, B, or C
            joined = ", ".join(recipe_names[:-1])
            return f"You could cook {joined}, or {recipe_names[-1]}."
