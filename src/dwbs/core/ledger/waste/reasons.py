from enum import Enum

class WasteReason(str, Enum):
    """
    D1.6 Waste as First-Class Event
    Standardized reasons for waste to allow analytics.
    """
    EXPIRED = "EXPIRED"
    SPILLED = "SPILLED"
    BAD_TASTE = "BAD_TASTE"
    OTHER = "OTHER"
