from abc import ABC, abstractmethod
from typing import List, Iterator
from ..events.types import LedgerEvent

class LedgerStore(ABC):
    """
    D1.1 Event-Sourcing Lite
    Interface for the append-only event store.
    """

    @abstractmethod
    def append(self, event: LedgerEvent) -> None:
        """
        Appends a new event to the ledger.
        Must enforce append-only logic (no overwrites).
        """
        pass

    @abstractmethod
    def get_stream(self) -> Iterator[LedgerEvent]:
        """
        Returns an iterator over the event stream chronologically.
        """
        pass

    @abstractmethod
    def snapshot(self) -> List[LedgerEvent]:
        """
        Returns a point-in-time copy of the full event log.
        """
        pass
