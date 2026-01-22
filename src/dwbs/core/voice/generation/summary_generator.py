from typing import List
from ...contracts.inventory import InventoryItem

class DailySummaryGenerator:
    """
    D9.1 Daily spoken summary
    """

    def generate_daily_summary(self, expiring_items: List[InventoryItem]) -> str:
        """
        Generates a text script for daily summary.
        """
        if not expiring_items:
            return "Good morning! You have no items expiring soon. Have a great day!"

        count = len(expiring_items)
        if count == 1:
            item_name = expiring_items[0].item.full_name()
            return f"Good morning! You have 1 item, {item_name}, expiring soon."

        return f"Good morning! You have {count} items expiring soon, including {expiring_items[0].item.name}."
