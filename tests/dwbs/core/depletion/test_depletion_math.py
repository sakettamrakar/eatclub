import pytest
from decimal import Decimal
from src.dwbs.core.ledger.store.memory import InMemoryLedgerStore
from src.dwbs.core.depletion.service import DepletionService
from src.dwbs.core.ledger.correction.undo import UndoService
from src.dwbs.core.recipe.domain.recipe import Recipe
from src.dwbs.core.recipe.domain.ingredient import IngredientRef
from src.dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit

class TestDepletionAccuracy:
    """
    P2-T13: Validate Depletion Accuracy
    """

    def setup_method(self):
        self.ledger = InMemoryLedgerStore()
        self.depletion_service = DepletionService()
        self.undo_service = UndoService()

    def test_zero_variance_undo(self):
        # Setup Recipe
        ingredient = IngredientRef(
            item=ItemIdentity(name="Flour"),
            quantity=Quantity(value=Decimal("1.5"), unit=Unit.KILOGRAM)
        )
        recipe = Recipe(id="rec-acc", name="Cake", ingredients=[ingredient], instructions=[])

        # 1. Deplete
        result_deplete = self.depletion_service.deplete_recipe(recipe, "user")
        assert result_deplete.is_success
        consume_event = result_deplete.value[0]

        self.ledger.append(consume_event)

        # 2. Undo
        result_undo = self.undo_service.undo_consumption(self.ledger, str(consume_event.event_id), "user")
        assert result_undo.is_success
        undo_event = result_undo.value

        # 3. Verify Math
        consumed_qty = consume_event.payload.quantity.value
        restored_qty = undo_event.payload.quantity_delta.value

        # Exact Match (Decimal)
        assert consumed_qty == restored_qty
        assert (consumed_qty - restored_qty) == Decimal("0")

    def test_partial_depletion_math(self):
        ingredient = IngredientRef(
            item=ItemIdentity(name="Sugar"),
            quantity=Quantity(value=Decimal("100"), unit=Unit.GRAM)
        )
        recipe = Recipe(id="rec-acc-2", name="Sweet", ingredients=[ingredient], instructions=[])

        factor = 0.333
        result = self.depletion_service.deplete_recipe(recipe, "user", factor=factor)

        event = result.value[0]
        expected = Decimal("100") * Decimal(str(factor))
        actual = event.payload.quantity.value

        assert actual == expected
