from decimal import Decimal
from typing import List
from ..contracts.failure import Result, ErrorCode
from ..recipe.domain.recipe import Recipe
from ..ledger.events.types import ConsumeEvent, ConsumePayload
from ..contracts.mutation import MutationSource
from ..contracts.explanation import Explanation
from ..contracts.inventory import Quantity

class DepletionService:
    """
    D8.1 Recipe-linked depletion
    D8.2 Partial consumption logic
    """

    def deplete_recipe(self, recipe: Recipe, actor_id: str, factor: float = 1.0) -> Result[List[ConsumeEvent]]:
        """
        Calculates required ingredients for a recipe and creates drafted ConsumeEvents.
        Supports partial consumption via factor (e.g. 0.5 for half recipe).
        """
        if not recipe:
            return Result.fail(ErrorCode.MISSING_DATA, "Recipe is None")

        if factor < 0:
             return Result.fail(ErrorCode.INVALID_STATE, "Factor must be non-negative")

        events = []
        # Convert to Decimal safely. Handle float precision issues by string conversion if needed.
        # But simple float to Decimal might have artifacts. using str() is safer.
        factor_decimal = Decimal(str(factor))

        for ingredient in recipe.ingredients:
            # Apply factor
            new_quantity_value = ingredient.quantity.value * factor_decimal
            new_quantity = Quantity(
                value=new_quantity_value,
                unit=ingredient.quantity.unit,
                approx=ingredient.quantity.approx
            )

            explanation = Explanation(
                reason=f"Cooking: {recipe.name} (x{factor})",
                source_fact=f"Recipe:{recipe.id}",
                confidence=1.0
            )

            payload = ConsumePayload(
                item=ingredient.item,
                quantity=new_quantity,
                source=MutationSource.USER_MANUAL,
                explanation=explanation
            )

            event = ConsumeEvent(
                actor=actor_id,
                payload=payload
            )
            events.append(event)

        return Result.success(events)
