from typing import List, Set
from datetime import date
from pydantic import Field
from ...contracts.base import SystemContract
from ...contracts.failure import Result
from ...ledger.events.types import LedgerEvent, ConsumeEvent

class PlannedMeal(SystemContract):
    recipe_id: str
    recipe_name: str
    planned_date: date

class MissedMealSuggestion(SystemContract):
    planned_meal: PlannedMeal
    message: str

class ReconciliationService:
    """
    D8.3 Missed-meal reconciliation
    """

    def check_missed_meals(self,
                           planned_meals: List[PlannedMeal],
                           ledger_events: List[LedgerEvent]) -> Result[List[MissedMealSuggestion]]:
        """
        Identifies planned meals that do not have a corresponding ConsumeEvent.
        """
        suggestions = []

        # Extract consumed recipe IDs from ledger
        consumed_recipe_ids = set()
        for event in ledger_events:
            if isinstance(event, ConsumeEvent):
                # Check explanation for source_fact "Recipe:{id}"
                if event.payload.explanation and event.payload.explanation.source_fact.startswith("Recipe:"):
                    parts = event.payload.explanation.source_fact.split(":")
                    if len(parts) >= 2:
                        recipe_id = parts[1]
                        consumed_recipe_ids.add(recipe_id)

        today = date.today()

        for meal in planned_meals:
            # Check strictly past meals (or we can include today if we assume it should be done by now, but safer to check past)
            # Task says "Identify undeleted planned meals".
            # If it's in the past and not consumed, it's missed.
            if meal.planned_date < today:
                if meal.recipe_id not in consumed_recipe_ids:
                    # Not found in consumption logs.
                    suggestions.append(MissedMealSuggestion(
                        planned_meal=meal,
                        message=f"Did you make {meal.recipe_name} on {meal.planned_date}?"
                    ))

        return Result.success(suggestions)
