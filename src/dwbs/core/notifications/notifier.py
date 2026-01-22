from typing import Optional
from ..ledger.events.types import LedgerEvent, MutationType

class Notification:
    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body

class Notifier:
    """
    D10.4 Notification rules
    """

    def generate_notification(self, event: LedgerEvent, current_user_id: str) -> Optional[Notification]:
        """
        Generate in-app alert when another user updates inventory.
        """
        if not event:
            return None

        if event.actor == current_user_id:
            return None # Don't notify self

        # Logic to generate message
        actor_name = event.actor or "Someone"

        item_name = "an item"
        if hasattr(event, 'payload') and hasattr(event.payload, 'item'):
            item_name = event.payload.item.name

        if event.mutation_type == MutationType.PURCHASE:
            return Notification("Inventory Update", f"{actor_name} added {item_name}.")
        elif event.mutation_type == MutationType.CONSUME:
             return Notification("Inventory Update", f"{actor_name} used {item_name}.")

        return Notification("Inventory Update", f"{actor_name} updated the inventory.")
