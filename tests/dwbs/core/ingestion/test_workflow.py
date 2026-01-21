import unittest
from unittest.mock import Mock, MagicMock
from dwbs.core.ingestion.workflow.confirmation import DraftConfirmationService
from dwbs.core.ledger.store.interface import LedgerStore
from dwbs.core.ingestion.draft.schema import DraftItem
from dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit
from dwbs.core.ledger.events.types import PurchaseEvent
from dwbs.core.contracts.mutation import MutationSource

class TestDraftConfirmationService(unittest.TestCase):
    def setUp(self):
        self.mock_store = Mock(spec=LedgerStore)
        self.service = DraftConfirmationService(self.mock_store)

    def test_finalize_draft(self):
        # Setup draft items
        item_id = ItemIdentity(name="Apple", confidence=1.0)
        qty = Quantity(value=1.0, unit=Unit.PIECE)
        draft = DraftItem(item=item_id, quantity=qty)

        # Execute
        events = self.service.finalize_draft([draft], actor="tester")

        # Assert
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertIsInstance(event, PurchaseEvent)
        self.assertEqual(event.actor, "tester")
        self.assertEqual(event.payload.item.name, "Apple")
        self.assertEqual(event.payload.source, MutationSource.USER_CONFIRMED_OCR)

        self.mock_store.append.assert_called_once_with(event)

    def test_finalize_empty_list(self):
        events = self.service.finalize_draft([])
        self.assertEqual(len(events), 0)
        self.mock_store.append.assert_not_called()

if __name__ == '__main__':
    unittest.main()
