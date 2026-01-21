from typing import List, Iterator
from .interface import LedgerStore
from ..events.types import LedgerEvent

class InMemoryLedgerStore(LedgerStore):
    """
    D1.1 Event-Sourcing Lite
    In-memory implementation of the LedgerStore.
    """
    def __init__(self):
        self._events: List[LedgerEvent] = []

    def append(self, event: LedgerEvent) -> None:
        if not isinstance(event, LedgerEvent):
            raise TypeError("Only LedgerEvent instances can be appended.")
        # Strictly append-only.
        self._events.append(event)

    def get_stream(self) -> Iterator[LedgerEvent]:
        # Return iterator to prevent modification of the list
        return iter(self._events)

    def snapshot(self) -> List[LedgerEvent]:
        # Return a shallow copy of the list
        return list(self._events)
