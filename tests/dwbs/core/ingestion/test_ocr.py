import unittest
from dwbs.core.ingestion.ocr.provider import MockOcrProvider
from dwbs.core.ingestion.draft.schema import DraftSession

class TestOcrProvider(unittest.TestCase):
    def test_mock_ocr_returns_drafts(self):
        provider = MockOcrProvider()
        image_data = b"fake_image_bytes"
        session_id = "sess-ocr-1"

        session = provider.process_image(image_data, session_id)

        self.assertIsInstance(session, DraftSession)
        self.assertEqual(session.session_id, session_id)
        self.assertEqual(session.source, "MockOCR")
        self.assertEqual(len(session.items), 2)

        # Verify confidence is 0.4
        self.assertEqual(session.items[0].item.confidence, 0.4)
        self.assertEqual(session.items[1].item.confidence, 0.4)

if __name__ == '__main__':
    unittest.main()
