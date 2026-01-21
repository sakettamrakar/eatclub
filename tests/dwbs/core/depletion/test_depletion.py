import pytest
from decimal import Decimal
from src.dwbs.core.recipe.domain.recipe import Recipe
from src.dwbs.core.recipe.domain.ingredient import IngredientRef
from src.dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit
from src.dwbs.core.depletion.service import DepletionService

class TestDepletionService:
    def setup_method(self):
        self.service = DepletionService()

    def test_deplete_recipe_simple(self):
        ingredient1 = IngredientRef(
            item=ItemIdentity(name="Pasta"),
            quantity=Quantity(value=Decimal("500"), unit=Unit.GRAM)
        )
        recipe = Recipe(
            id="rec-001",
            name="Pasta Carbonara",
            ingredients=[ingredient1],
            instructions=["Boil pasta"]
        )

        result = self.service.deplete_recipe(recipe, actor_id="user-1")
        assert result.is_success
        events = result.value
        assert len(events) == 1

        event = events[0]
        assert event.payload.item.name == "Pasta"
        assert event.payload.quantity.value == Decimal("500")
        assert event.payload.explanation.reason == "Cooking: Pasta Carbonara (x1.0)"
        assert event.actor == "user-1"

    def test_deplete_recipe_partial(self):
        ingredient1 = IngredientRef(
            item=ItemIdentity(name="Pasta"),
            quantity=Quantity(value=Decimal("500"), unit=Unit.GRAM)
        )
        recipe = Recipe(
            id="rec-001",
            name="Pasta Carbonara",
            ingredients=[ingredient1],
            instructions=["Boil pasta"]
        )

        # Half portion
        result = self.service.deplete_recipe(recipe, actor_id="user-1", factor=0.5)
        assert result.is_success
        events = result.value
        event = events[0]
        assert event.payload.quantity.value == Decimal("250.0") # 500 * 0.5
        assert event.payload.explanation.reason == "Cooking: Pasta Carbonara (x0.5)"

    def test_deplete_recipe_empty(self):
        result = self.service.deplete_recipe(None, "user-1")
        assert result.is_failure
