from typing import List, Optional
from ..domain.recipe import Recipe
from .tags import RecipeTag

def filter_recipes(recipes: List[Recipe], required_tags: Optional[List[RecipeTag]] = None, exclude_tags: Optional[List[RecipeTag]] = None) -> List[Recipe]:
    """
    Filters a list of recipes based on tags.
    - required_tags: Recipe must include ALL of these tags.
    - exclude_tags: Recipe must include NONE of these tags.
    """
    if not required_tags and not exclude_tags:
        return recipes

    result = []
    for recipe in recipes:
        recipe_tags = set(recipe.tags)

        if required_tags:
            # Check if all required tags are present
            if not all(tag in recipe_tags for tag in required_tags):
                continue

        if exclude_tags:
            # Check if any excluded tag is present
            if any(tag in recipe_tags for tag in exclude_tags):
                continue

        result.append(recipe)

    return result
