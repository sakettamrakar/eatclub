import pytest
from datetime import date, timedelta
from src.dwbs.core.depletion.reconcile.service import ReconciliationService, PlannedMeal
from src.dwbs.core.ledger.events.types import ConsumeEvent, ConsumePayload, MutationType
from src.dwbs.core.contracts.mutation import MutationSource
from src.dwbs.core.contracts.explanation import Explanation
from src.dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit
from decimal import Decimal

class TestReconciliationService:
    def setup_method(self):
        self.service = ReconciliationService()

    def create_consume_event(self, recipe_id: str) -> ConsumeEvent:
        return ConsumeEvent(
            actor="user",
            payload=ConsumePayload(
                item=ItemIdentity(name="Test"),
                quantity=Quantity(value=Decimal(1), unit=Unit.PIECE),
                source=MutationSource.USER_MANUAL,
                explanation=Explanation(
                    reason="Cooking",
                    source_fact=f"Recipe:{recipe_id}",
                    confidence=1.0
                )
            )
        )

    def test_detect_missed_meal(self):
        past_date = date.today() - timedelta(days=1)
        planned = PlannedMeal(recipe_id="rec-1", recipe_name="Pizza", planned_date=past_date)

        # Ledger has no events
        result = self.service.check_missed_meals([planned], [])
        assert result.is_success
        suggestions = result.value
        assert len(suggestions) == 1
        assert "Did you make Pizza" in suggestions[0].message

    def test_no_missed_meal_if_consumed(self):
        past_date = date.today() - timedelta(days=1)
        planned = PlannedMeal(recipe_id="rec-1", recipe_name="Pizza", planned_date=past_date)

        event = self.create_consume_event("rec-1")

        result = self.service.check_missed_meals([planned], [event])
        assert result.is_success
        suggestions = result.value
        assert len(suggestions) == 0

    def test_ignore_future_meals(self):
        future_date = date.today() + timedelta(days=1)
        planned = PlannedMeal(recipe_id="rec-2", recipe_name="Tacos", planned_date=future_date)

        result = self.service.check_missed_meals([planned], [])
        assert result.is_success
        assert len(result.value) == 0
