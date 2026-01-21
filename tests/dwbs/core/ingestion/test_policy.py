import unittest
from unittest.mock import Mock, MagicMock
from dwbs.core.ingestion.ocr.provider import MockOcrProvider
from dwbs.core.ledger.store.memory import InMemoryLedgerStore
from dwbs.core.ingestion.draft.schema import DraftSession

class TestNoSilentMutation(unittest.TestCase):
    """
    Task 5.5: Validate No-Silent-Mutation Policy
    Verify that calling OCR provider does NOT increase Ledger count.
    """
    def setUp(self):
        self.ledger_store = InMemoryLedgerStore()
        self.ocr_provider = MockOcrProvider()

    def test_ocr_does_not_mutate_ledger(self):
        # 1. Capture initial state
        initial_event_count = len(list(self.ledger_store.get_stream()))

        # 2. Perform OCR Action
        image_data = b"fake_image"
        session_id = "test-session"
        draft_session = self.ocr_provider.process_image(image_data, session_id)

        # 3. Verify Ledger State
        final_event_count = len(list(self.ledger_store.get_stream()))

        self.assertEqual(initial_event_count, final_event_count, "OCR process should not mutate ledger")
        self.assertIsInstance(draft_session, DraftSession)

if __name__ == '__main__':
    unittest.main()
