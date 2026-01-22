from typing import Optional
from enum import Enum
from ...contracts.failure import Result, ErrorCode
from ...ledger.events.types import LedgerEvent

class ResolutionChoice(str, Enum):
    KEEP_LOCAL = "KEEP_LOCAL"
    ACCEPT_REMOTE = "ACCEPT_REMOTE"

class ConflictResolver:
    """
    D10.2 Conflict Resolution
    """

    def resolve_conflict(self, local_event: LedgerEvent, remote_event: LedgerEvent, choice: ResolutionChoice) -> Result[LedgerEvent]:
        """
        Resolves conflict between two events (versions) based on user choice.
        Returns the event that should be applied.
        """
        if not local_event or not remote_event:
            return Result.fail(ErrorCode.MISSING_DATA, "Events cannot be None")

        if choice == ResolutionChoice.KEEP_LOCAL:
            # We need to re-version local event to match expected remote sequence?
            # Or simply return the winner.
            # In a real system, we'd need to rebase.
            # Here we just return the winner.
            return Result.success(local_event)
        elif choice == ResolutionChoice.ACCEPT_REMOTE:
            return Result.success(remote_event)

        return Result.fail(ErrorCode.INVALID_STATE, "Invalid choice")
