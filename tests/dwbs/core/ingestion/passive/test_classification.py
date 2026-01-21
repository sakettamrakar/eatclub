import pytest
from datetime import datetime
from src.dwbs.core.ingestion.passive.email.types import EmailSignal
from src.dwbs.core.ingestion.passive.classification.types import InvoiceType
from src.dwbs.core.ingestion.passive.classification.classifier import InvoiceClassifier

class TestInvoiceClassifier:
    def setup_method(self):
        self.classifier = InvoiceClassifier()

    def create_signal(self, subject: str, sender: str) -> EmailSignal:
        return EmailSignal(
            message_id="test-id",
            sender=sender,
            subject=subject,
            received_at=datetime.now(),
            body_text="Some body text"
        )

    def test_classify_grocery_invoice(self):
        signal = self.create_signal("Your Order #12345", "orders@grocery.com")
        result = self.classifier.classify_email(signal)
        assert result.is_success
        assert result.value == InvoiceType.GROCERY_INVOICE

    def test_classify_junk(self):
        signal = self.create_signal("Weekly Sale Alert", "marketing@store.com")
        result = self.classifier.classify_email(signal)
        assert result.is_success
        assert result.value == InvoiceType.JUNK

    def test_classify_unknown(self):
        signal = self.create_signal("Meeting Reminder", "boss@work.com")
        result = self.classifier.classify_email(signal)
        assert result.is_success
        assert result.value == InvoiceType.UNKNOWN

    def test_classify_grocery_priority(self):
        # If it has both (e.g. "Order Alert"), it should probably be grocery if "Order" is stronger?
        # My logic checks Grocery first.
        signal = self.create_signal("Your Order has a Sale Item", "orders@store.com")
        result = self.classifier.classify_email(signal)
        assert result.value == InvoiceType.GROCERY_INVOICE
