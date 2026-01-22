from typing import Optional
from datetime import date
from ...contracts.inventory import InventoryItem

class ExpiryAlertGenerator:
    """
    D9.2 Expiry alerts
    """

    def generate_expiry_alert(self, item: InventoryItem) -> Optional[str]:
        """
        Generate text for urgent expiry.
        """
        # We need to bypass `is_in_stock` check for expired items because `is_in_stock` returns False if expired.
        # But we want to alert "Your item has expired".
        if not item or not item.expiry_date:
            return None

        # Check quantity > 0 regardless of expiry
        if item.quantity.value <= 0:
            return None

        days_remaining = (item.expiry_date - date.today()).days

        # Only alert for items expiring today or tomorrow (or already expired)
        if days_remaining < 0:
            return f"Your {item.item.name} has expired."
        elif days_remaining == 0:
            return f"Use your {item.item.name} by today."
        elif days_remaining == 1:
            return f"Use your {item.item.name} by tomorrow."

        return None
