import pytest
from decimal import Decimal
from src.dwbs.core.contracts.inventory import InventoryItem, ItemIdentity, Quantity, Unit
from src.dwbs.core.voice.generation.summary_generator import DailySummaryGenerator
from src.dwbs.core.voice.generation.alert_generator import ExpiryAlertGenerator
from src.dwbs.core.voice.generation.suggestion_formatter import SpokenSuggestionFormatter
from src.dwbs.core.recipe.domain.recipe import Recipe

class TestVoiceSafety:
    """
    P2-T18: Validate Voice Output Safety
    Verify voice logic ONLY reads state and NEVER mutates it.
    """

    def setup_method(self):
        self.summary_gen = DailySummaryGenerator()
        self.alert_gen = ExpiryAlertGenerator()
        self.suggestion_fmt = SpokenSuggestionFormatter()

    def test_summary_does_not_mutate_items(self):
        item = InventoryItem(
            item=ItemIdentity(name="Milk"),
            quantity=Quantity(value=Decimal(1), unit=Unit.LITER)
        )
        original_qty = item.quantity.value

        _ = self.summary_gen.generate_daily_summary([item])

        assert item.quantity.value == original_qty

    def test_alert_does_not_mutate_item(self):
        item = InventoryItem(
            item=ItemIdentity(name="Milk"),
            quantity=Quantity(value=Decimal(1), unit=Unit.LITER)
        )
        original_qty = item.quantity.value

        _ = self.alert_gen.generate_expiry_alert(item)

        assert item.quantity.value == original_qty

    def test_suggestion_does_not_mutate_recipe(self):
        recipe = Recipe(id="1", name="Pizza", ingredients=[], instructions=[])
        original_name = recipe.name

        _ = self.suggestion_fmt.format_suggestions([recipe])

        assert recipe.name == original_name
