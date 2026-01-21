from ...ledger.events.types import ConsumeEvent, CorrectionAddEvent, CorrectionPayload, MutationType
from ...ledger.store.interface import LedgerStore
from ...contracts.failure import Result, ErrorCode
from ...contracts.mutation import MutationSource
from ...contracts.explanation import Explanation

class UndoService:
    """
    D8.4 Undo + correction system
    """

    def undo_consumption(self, ledger: LedgerStore, event_id: str, actor_id: str) -> Result[CorrectionAddEvent]:
        """
        Creates a CorrectionAddEvent to reverse a ConsumeEvent.
        Blocks if the item has been modified since the target event.
        """
        # Find event
        target_event = None
        stream = list(ledger.get_stream()) # Materialize once

        target_index = -1
        for i, event in enumerate(stream):
            if str(event.event_id) == str(event_id):
                target_event = event
                target_index = i
                break

        if not target_event:
             return Result.fail(ErrorCode.MISSING_DATA, "Event not found")

        if not isinstance(target_event, ConsumeEvent):
             return Result.fail(ErrorCode.INVALID_STATE, "Target event is not a ConsumeEvent")

        # Check if stock modified since
        target_item = target_event.payload.item

        # Check events AFTER target_index
        for i in range(target_index + 1, len(stream)):
            event = stream[i]
            if hasattr(event, 'payload') and hasattr(event.payload, 'item'):
                if event.payload.item == target_item:
                     return Result.fail(ErrorCode.INVALID_STATE, "Item modified since consumption. Undo blocked.")

        # Create correction
        correction_payload = CorrectionPayload(
            item=target_item,
            quantity_delta=target_event.payload.quantity, # Add back what was consumed
            source=MutationSource.USER_MANUAL,
            explanation=Explanation(
                reason="Undo Consumption",
                source_fact=f"Undo:{event_id}",
                confidence=1.0
            )
        )

        correction_event = CorrectionAddEvent(
            actor=actor_id,
            payload=correction_payload
        )

        return Result.success(correction_event)
