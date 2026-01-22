import pytest
from src.dwbs.core.auth.roles import UserRole, PermissionChecker
from src.dwbs.core.contracts.mutation import MutationType

class TestRoleEnforcement:
    """
    P2-T25: Implement Role Enforcement Tests
    Strict tests to ensure `VIEWER` role can NEVER call `applyMutation`.
    """

    def setup_method(self):
        self.checker = PermissionChecker()

    def test_viewer_denial(self):
        # Ensure VIEWER is denied for ALL mutation types defined in system
        for mutation in MutationType:
            result = self.checker.check_permission(UserRole.VIEWER, mutation)
            assert result.is_failure, f"Viewer should not have permission for {mutation}"
            assert result.error.code == "CONTRACT_VIOLATION"

    def test_editor_limitations(self):
        # Editor cannot correct ledger history
        assert self.checker.check_permission(UserRole.EDITOR, MutationType.CORRECTION_ADD).is_failure
        assert self.checker.check_permission(UserRole.EDITOR, MutationType.CORRECTION_REMOVE).is_failure

        # Editor cannot snapshot
        assert self.checker.check_permission(UserRole.EDITOR, MutationType.SNAPSHOT).is_failure

    def test_admin_omni(self):
        # Admin must have access to everything
        for mutation in MutationType:
            assert self.checker.check_permission(UserRole.ADMIN, mutation).is_success
