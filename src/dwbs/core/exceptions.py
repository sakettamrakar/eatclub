class DWBSException(Exception):
    """Base exception for DWBS application."""
    pass

class InventoryError(DWBSException):
    """Base exception for inventory related errors."""
    pass

class InvalidInventoryStateError(InventoryError):
    """Raised when inventory is in an invalid state (e.g. negative quantity)."""
    pass

class ItemNotFoundError(InventoryError):
    """Raised when an item is not found in the inventory."""
    pass

class MutationError(InventoryError):
    """Raised when an inventory mutation is invalid or unauthorized."""
    pass

class ContractViolationError(DWBSException):
    """Raised when a system contract is violated."""
    pass

class UncertaintyError(DWBSException):
    """Raised when the system is too uncertain to proceed (Truth Before Utility)."""
    pass

class ConcurrencyError(DWBSException):
    """Raised when an optimistic locking check fails."""
    pass
