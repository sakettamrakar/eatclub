from enum import Enum
from typing import Set, TYPE_CHECKING
from ..contracts.failure import Result, ErrorCode
from ..contracts.mutation import MutationType

class UserRole(str, Enum):
    """
    D10.1 Roles (viewer/editor)
    """
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"

class PermissionChecker:
    """
    D10.1 Roles (viewer/editor)
    Checks permissions before mutation.
    """

    # Define allowed mutation types per role
    ALLOWED_MUTATIONS = {
        UserRole.ADMIN: {
            MutationType.PURCHASE, MutationType.CONSUME, MutationType.WASTE,
            MutationType.CORRECTION_ADD, MutationType.CORRECTION_REMOVE, MutationType.SNAPSHOT
        },
        UserRole.EDITOR: {
            MutationType.PURCHASE, MutationType.CONSUME, MutationType.WASTE
        },
        UserRole.VIEWER: set() # Empty set
    }

    def check_permission(self, role: UserRole, mutation_type: MutationType) -> Result[bool]:
        """
        Returns Success(True) if allowed, Failure if denied.
        """
        allowed = self.ALLOWED_MUTATIONS.get(role, set())

        if mutation_type in allowed:
            return Result.success(True)

        return Result.fail(
            ErrorCode.CONTRACT_VIOLATION,
            f"User with role {role.value} is not authorized to perform {mutation_type.value}"
        )
