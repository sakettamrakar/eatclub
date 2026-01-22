import pytest
from decimal import Decimal
import random
from src.dwbs.core.ledger.store.memory import InMemoryLedgerStore
from src.dwbs.core.depletion.service import DepletionService
from src.dwbs.core.ledger.correction.undo import UndoService
from src.dwbs.core.recipe.domain.recipe import Recipe
from src.dwbs.core.recipe.domain.ingredient import IngredientRef
from src.dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit

class TestDepletionReversibilityFuzz:
    """
    P2-T26: Implement Depletion Reversibility Tests
    Fuzz testing of Undo/Redo to ensure inventory count never drifts.
    """

    def setup_method(self):
        self.ledger = InMemoryLedgerStore()
        self.depletion = DepletionService()
        self.undo = UndoService()

    def test_random_deplete_undo_cycles(self):
        # Setup
        base_qty = Decimal("1000")
        item_name = "Rice"
        ingredient = IngredientRef(
            item=ItemIdentity(name=item_name),
            quantity=Quantity(value=Decimal("100"), unit=Unit.GRAM)
        )
        recipe = Recipe(id="fuzz-rec", name="Bowl", ingredients=[ingredient], instructions=[])

        cycles = 50
        net_change = Decimal("0")

        for _ in range(cycles):
            action = random.choice(["deplete", "deplete_undo"])

            if action == "deplete":
                # Consume 100g
                events = self.depletion.deplete_recipe(recipe, "user").value
                for e in events:
                    self.ledger.append(e)
                    net_change -= e.payload.quantity.value

            elif action == "deplete_undo":
                # Consume then immediately undo
                events = self.depletion.deplete_recipe(recipe, "user").value
                consume_event = events[0]
                self.ledger.append(consume_event)

                # Undo
                correction_result = self.undo.undo_consumption(self.ledger, str(consume_event.event_id), "user")
                if correction_result.is_success:
                    self.ledger.append(correction_result.value)
                    # Net change should be 0 for this cycle
                else:
                    # Should not happen in this controlled loop
                    pytest.fail("Undo failed in fuzz loop")

        # Verify Integrity
        # Replay ledger to calculate final stock of Rice
        final_stock = Decimal("0")
        for event in self.ledger.get_stream():
            if event.payload.item.name == item_name:
                if event.mutation_type == "CONSUME":
                    final_stock -= event.payload.quantity.value
                elif event.mutation_type == "CORRECTION_ADD":
                    final_stock += event.payload.quantity_delta.value

        assert final_stock == net_change
