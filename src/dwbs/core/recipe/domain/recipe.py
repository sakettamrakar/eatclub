from typing import List, Optional
from pydantic import Field
from ...contracts.base import SystemContract
from .ingredient import IngredientRef
from ..tags.tags import RecipeTag
from .metadata import Difficulty

class Recipe(SystemContract):
    """
    D2.1 Structured Ingredient Mappings
    Represents a cooking recipe.
    """
    id: str = Field(..., description="Unique identifier for the recipe.")
    name: str = Field(..., description="Display name of the recipe.")
    description: str = Field("", description="Short description.")
    ingredients: List[IngredientRef] = Field(..., description="List of ingredients required.")
    instructions: List[str] = Field(..., description="Step-by-step instructions.")
    tags: List[RecipeTag] = Field(default_factory=list, description="Cultural and context tags.")

    # D2.4 Operational Metadata
    prep_time_minutes: Optional[int] = Field(None, description="Preparation time in minutes.")
    cook_time_minutes: Optional[int] = Field(None, description="Cooking time in minutes.")
    difficulty: Optional[Difficulty] = Field(None, description="Difficulty level.")

    # Recursive composition: A recipe can be a component of another via ingredients,
    # or explicitly if we wanted, but sticking to IngredientRef + separate Recipes is safer for normalized data.
    # However, to explicitly support "Recipe in Recipe" as a structure:
    # We might want to allow ingredients to be defined inline, but that complicates things.
    # I will assume 'ingredients' covers it via ItemIdentity resolution.
