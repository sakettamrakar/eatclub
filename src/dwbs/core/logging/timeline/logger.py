from typing import List, Optional
from datetime import datetime
from pydantic import Field
from ...contracts.base import SystemContract
from ...ledger.events.types import LedgerEvent, MutationType

class ActivityLogEntry(SystemContract):
    timestamp: datetime
    actor: str
    action_type: str
    description: str

class TimelineLogger:
    """
    D10.3 Activity timeline
    """

    def log_activity(self, event: LedgerEvent) -> Optional[ActivityLogEntry]:
        """
        Aggregates view of LedgerEvents showing "Who did what".
        Returns None if event is not suitable for timeline.
        """
        if not event:
            return None

        description = self._generate_description(event)

        return ActivityLogEntry(
            timestamp=event.timestamp,
            actor=event.actor or "Unknown",
            action_type=event.mutation_type.value,
            description=description
        )

    def _generate_description(self, event: LedgerEvent) -> str:
        # Basic description generation based on event type and payload
        item_name = "Unknown Item"
        if hasattr(event, 'payload') and hasattr(event.payload, 'item'):
            item_name = event.payload.item.full_name()

        if event.mutation_type == MutationType.PURCHASE:
            return f"Purchased {item_name}"
        elif event.mutation_type == MutationType.CONSUME:
            return f"Consumed {item_name}"
        elif event.mutation_type == MutationType.WASTE:
            return f"Wasted {item_name}"
        elif event.mutation_type == MutationType.CORRECTION_ADD:
            return f"Corrected (Added) {item_name}"
        elif event.mutation_type == MutationType.CORRECTION_REMOVE:
            return f"Corrected (Removed) {item_name}"

        return "Performed unknown action"
