from enum import Enum
from typing import Generic, TypeVar, Optional, Union
from pydantic import BaseModel, ConfigDict
from .contracts import SystemContract, Explanation

T = TypeVar('T')

class ErrorCode(str, Enum):
    """
    D0.4 Failure Rules
    Standard error codes.
    """
    MISSING_DATA = "MISSING_DATA"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    AMBIGUOUS_INPUT = "AMBIGUOUS_INPUT"
    INVALID_STATE = "INVALID_STATE"
    CONTRACT_VIOLATION = "CONTRACT_VIOLATION"
    SYSTEM_ERROR = "SYSTEM_ERROR"

class Outcome(SystemContract, Generic[T]):
    """
    D0.4 Failure Rules
    Wrapper for all core operation results.
    """
    success: bool
    data: Optional[T] = None
    error_code: Optional[ErrorCode] = None
    message: Optional[str] = None
    explanation: Optional[Explanation] = None

    @classmethod
    def ok(cls, data: T, explanation: Optional[Explanation] = None) -> 'Outcome[T]':
        return cls(success=True, data=data, explanation=explanation)

    @classmethod
    def fail(cls, code: ErrorCode, message: str, explanation: Optional[Explanation] = None) -> 'Outcome[T]':
        return cls(success=False, error_code=code, message=message, explanation=explanation)

    def unwrap(self) -> T:
        """
        Unsafe unwrap. Raises exception if failed.
        """
        if not self.success:
            raise RuntimeError(f"Outcome failed: {self.error_code} - {self.message}")
        # data CAN be None if T is NoneType or Optional, but here we assume success implies data presence for most cases.
        # But technically T could be None.
        return self.data
