from datetime import date, timedelta
from typing import Dict, Optional
from ..identity.resolution import ItemIdentity

class ExpiryCalculator:
    """
    D1.5 Expiry & Purchase Tracking
    Deterministic expiry calculation using a static lookup table.
    """

    # Static lookup table (Phase 1 kernel)
    # Days from purchase. Keys are item names.
    _SHELF_LIFE_DAYS: Dict[str, int] = {
        "Tomato": 7,
        "Lettuce": 5,
        "Milk": 7,
        "Eggs": 21,
        "Rice": 365,
        "Pasta": 365,
        "Chicken": 2, # Raw
    }

    _DEFAULT_DAYS = 3 # Conservative default for unknowns

    @classmethod
    def predict_expiry(cls, item: ItemIdentity, purchase_date: date) -> date:
        """
        Predicts expiry date based on item name and purchase date.
        """
        # Lookup by name (ignoring variant for simple Phase 1 lookup, or we could map (name, variant))
        # Logic: If variant suggests preservation (Canned, Frozen), we should handle it.
        # But for now, simple table lookup as per Task 2.6 requirements.

        days = cls._SHELF_LIFE_DAYS.get(item.name)

        if days is None:
            days = cls._DEFAULT_DAYS

        return purchase_date + timedelta(days=days)
