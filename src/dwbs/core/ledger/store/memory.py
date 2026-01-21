from typing import List, Iterator
from .interface import LedgerStore
from ..events.types import LedgerEvent
from ...exceptions import ConcurrencyError

class InMemoryLedgerStore(LedgerStore):
    """
    D1.1 Event-Sourcing Lite
    In-memory implementation of the LedgerStore.
    """
    def __init__(self):
        self._events: List[LedgerEvent] = []
        self._current_version: int = 0

    def append(self, event: LedgerEvent) -> None:
        if not isinstance(event, LedgerEvent):
            raise TypeError("Only LedgerEvent instances can be appended.")

        # Optimistic Locking Check
        if event.expected_version is not None:
            if event.expected_version != self._current_version:
                raise ConcurrencyError(
                    f"Version mismatch: Expected {event.expected_version}, but ledger is at {self._current_version}"
                )

        # Strictly append-only.
        self._events.append(event)
        self._current_version += 1

    def get_stream(self) -> Iterator[LedgerEvent]:
        # Return iterator to prevent modification of the list
        return iter(self._events)

    def snapshot(self) -> List[LedgerEvent]:
        # Return a shallow copy of the list
        return list(self._events)

    @property
    def version(self) -> int:
        return self._current_version
