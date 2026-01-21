import unittest
from datetime import date
from dwbs.core.ingestion.draft.schema import DraftItem, DraftSession
from dwbs.core.contracts.inventory import ItemIdentity, Quantity, Unit

class TestDraftSchema(unittest.TestCase):
    def test_draft_item_creation(self):
        item_id = ItemIdentity(name="Apple", confidence=0.4)
        qty = Quantity(value=1.0, unit=Unit.PIECE)
        draft = DraftItem(item=item_id, quantity=qty)

        self.assertEqual(draft.item.name, "Apple")
        self.assertEqual(draft.quantity.value, 1.0)
        self.assertIsNone(draft.expiry_date)

    def test_draft_session_creation(self):
        item_id = ItemIdentity(name="Apple", confidence=0.4)
        qty = Quantity(value=1.0, unit=Unit.PIECE)
        draft = DraftItem(item=item_id, quantity=qty)

        session = DraftSession(session_id="sess-1", items=[draft], source="OCR")

        self.assertEqual(session.session_id, "sess-1")
        self.assertEqual(len(session.items), 1)
        self.assertEqual(session.source, "OCR")

if __name__ == '__main__':
    unittest.main()
