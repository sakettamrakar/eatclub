from enum import Enum
from typing import List

class RecipeTag(str, Enum):
    """
    D2.3 Cultural & Context Tags
    """
    INDIAN = "Indian"
    ITALIAN = "Italian"
    BREAKFAST = "Breakfast"
    DINNER = "Dinner"
    QUICK = "Quick"
    TADKA_REQUIRED = "Tadka-Required"
    VEGETARIAN = "Vegetarian"
    VEGAN = "Vegan"
