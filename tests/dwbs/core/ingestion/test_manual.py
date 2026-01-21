import unittest
from unittest.mock import Mock, MagicMock
from dwbs.core.ingestion.manual.service import ManualEntryService
from dwbs.core.ledger.store.interface import LedgerStore
from dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit
from dwbs.core.ledger.events.types import PurchaseEvent
from dwbs.core.contracts.mutation import MutationSource

class TestManualEntryService(unittest.TestCase):
    def setUp(self):
        self.mock_store = Mock(spec=LedgerStore)
        self.service = ManualEntryService(self.mock_store)

    def test_create_entry(self):
        # Setup
        item_id = ItemIdentity(name="Apple", confidence=0.5) # User might pass low confidence obj
        qty = Quantity(value=1.0, unit=Unit.PIECE)

        # Execute
        event = self.service.create_entry(item_id, qty, actor="tester")

        # Assert
        self.assertIsInstance(event, PurchaseEvent)
        self.assertEqual(event.actor, "tester")
        self.assertEqual(event.payload.item.name, "Apple")
        self.assertEqual(event.payload.item.confidence, 1.0) # Should be forced to 1.0
        self.assertEqual(event.payload.source, MutationSource.USER_MANUAL)
        self.assertEqual(event.payload.explanation.reason, "Manual entry by user.")

        self.mock_store.append.assert_called_once_with(event)

if __name__ == '__main__':
    unittest.main()
