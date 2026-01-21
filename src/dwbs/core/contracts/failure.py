from enum import Enum
from typing import Generic, TypeVar, Optional
from pydantic import Field
from .base import SystemContract

T = TypeVar("T")

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
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

class Failure(SystemContract):
    """
    Structured failure information.
    """
    code: ErrorCode
    message: str
    details: Optional[str] = None

class Result(SystemContract, Generic[T]):
    """
    D0.4 Failure Rules
    Wrapper for operation outcomes.
    """
    value: Optional[T] = None
    error: Optional[Failure] = None

    @property
    def is_success(self) -> bool:
        return self.error is None

    @property
    def is_failure(self) -> bool:
        return self.error is not None

    @classmethod
    def success(cls, value: T) -> 'Result[T]':
        return cls(value=value)

    @classmethod
    def fail(cls, code: ErrorCode, message: str, details: str = None) -> 'Result[T]':
        return cls(error=Failure(code=code, message=message, details=details))
