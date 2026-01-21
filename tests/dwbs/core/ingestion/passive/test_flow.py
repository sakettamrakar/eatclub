import pytest
from datetime import datetime, date
from decimal import Decimal
from typing import List

from src.dwbs.core.contracts.mutation import MutationSource
from src.dwbs.core.contracts.explanation import Explanation
from src.dwbs.core.ledger.events.types import PurchaseEvent, PurchasePayload, MutationType
from src.dwbs.core.ledger.store.memory import InMemoryLedgerStore

from src.dwbs.core.ingestion.passive.email.types import EmailSignal
from src.dwbs.core.ingestion.passive.classification.types import InvoiceType
from src.dwbs.core.ingestion.passive.classification.classifier import InvoiceClassifier
from src.dwbs.core.ingestion.passive.parser.parser import TextParser
from src.dwbs.core.ingestion.passive.scoring.scorer import ConfidenceScorer

class TestPassiveIngestionFlow:
    """
    P2-T8: Validate Passive Signal Flow.
    End-to-end test: Mock Email -> Classify -> Parse -> Score -> UI Review -> Ledger.
    """

    def setup_method(self):
        self.classifier = InvoiceClassifier()
        self.parser = TextParser()
        self.scorer = ConfidenceScorer()
        self.ledger = InMemoryLedgerStore()

    def test_end_to_end_flow(self):
        # 1. Mock Email Signal
        email_body = """
        Milk 1 L
        Bread 2 PCS
        """
        signal = EmailSignal(
            message_id="msg-001",
            sender="orders@grocery.com",
            subject="Your Order #123",
            received_at=datetime.now(),
            body_text=email_body
        )

        # 2. Classify
        classification_result = self.classifier.classify_email(signal)
        assert classification_result.is_success
        assert classification_result.value == InvoiceType.GROCERY_INVOICE

        # 3. Parse
        if classification_result.value == InvoiceType.GROCERY_INVOICE:
            parse_result = self.parser.parse_text(signal.body_text)
            assert parse_result.is_success
            draft_items = parse_result.value
            assert len(draft_items) == 2
        else:
            pytest.fail("Email should be classified as Grocery")

        # 4. Score
        scored_items = self.scorer.score_drafts(draft_items, signal.sender)
        assert len(scored_items) == 2
        assert scored_items[0].item.confidence == 0.9  # Known vendor
        assert scored_items[0].item.name == "Milk"

        # 5. UI Logic / User Confirmation
        # Assume user confirms all items.
        # Create PurchaseEvents

        events = []
        for draft in scored_items:
            # Logic: Convert Draft to Event
            explanation = Explanation(
                reason="Imported from Email Invoice",
                source_fact=f"Email:{signal.message_id}",
                confidence=draft.item.confidence
            )

            payload = PurchasePayload(
                item=draft.item,
                quantity=draft.quantity,
                expiry_date=draft.expiry_date,
                source=MutationSource.USER_CONFIRMED_OCR, # Or similar source
                explanation=explanation
            )

            event = PurchaseEvent(
                actor="user-id", # Simulated user
                payload=payload
            )
            events.append(event)

        # 6. Commit to Ledger
        current_ledger_version_before = self.ledger.version
        for event in events:
            self.ledger.append(event)

        # 7. Verify Ledger
        assert self.ledger.version == current_ledger_version_before + 2

        stream = list(self.ledger.get_stream())
        assert len(stream) == 2

        event1 = stream[0]
        assert isinstance(event1, PurchaseEvent)
        assert event1.payload.item.name == "Milk"
        assert event1.payload.quantity.value == Decimal("1")
        assert event1.payload.explanation.source_fact == f"Email:{signal.message_id}"
