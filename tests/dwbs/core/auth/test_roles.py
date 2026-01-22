import pytest
from src.dwbs.core.auth.roles import UserRole, PermissionChecker
from src.dwbs.core.contracts.mutation import MutationType

class TestPermissionChecker:
    def setup_method(self):
        self.checker = PermissionChecker()

    def test_admin_permissions(self):
        # Admin can do everything
        for mutation in MutationType:
            result = self.checker.check_permission(UserRole.ADMIN, mutation)
            assert result.is_success

    def test_editor_permissions(self):
        # Editor can PURCHASE, CONSUME, WASTE
        assert self.checker.check_permission(UserRole.EDITOR, MutationType.PURCHASE).is_success
        assert self.checker.check_permission(UserRole.EDITOR, MutationType.CONSUME).is_success
        assert self.checker.check_permission(UserRole.EDITOR, MutationType.WASTE).is_success

        # Editor cannot CORRECT
        assert self.checker.check_permission(UserRole.EDITOR, MutationType.CORRECTION_ADD).is_failure
        assert self.checker.check_permission(UserRole.EDITOR, MutationType.CORRECTION_REMOVE).is_failure

    def test_viewer_permissions(self):
        # Viewer can do nothing
        for mutation in MutationType:
             assert self.checker.check_permission(UserRole.VIEWER, mutation).is_failure
