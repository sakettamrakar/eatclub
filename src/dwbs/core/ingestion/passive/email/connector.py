from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, timedelta, timezone
from .types import EmailSignal

class EmailConnector(ABC):
    """
    Abstract contract for Email Connectors.
    Enforces read-only access pattern.
    """

    @abstractmethod
    def connect(self) -> bool:
        """
        Establishes connection to the email provider.
        Returns True if successful.
        """
        pass

    @abstractmethod
    def fetch_signals(self, label: str, limit: int = 10) -> List[EmailSignal]:
        """
        Fetches basic metadata and content from emails with the given label.
        Does NOT modify the email state (read-only).
        """
        pass

class MockGmailConnector(EmailConnector):
    """
    Deterministic mock connector for validation and testing.
    Simulates a Gmail connection without external network calls.
    Used for Phase 2 validation where real credentials are not available.
    """

    def connect(self) -> bool:
        # Simulate successful authentication
        return True

    def fetch_signals(self, label: str, limit: int = 10) -> List[EmailSignal]:
        # Deterministic reference time
        base_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        signals = []

        # Scenario 1: Grocery Receipt (High confidence structure)
        signals.append(EmailSignal(
            message_id="mock_msg_001",
            sender="orders@freshmarket.com",
            subject="Your Receipt for Order #998877",
            received_at=base_time,
            snippet="Thank you for your purchase. Total: $45.50",
            body_text="Fresh Market\nDate: 2024-01-01\n\nItems:\n1. Organic Bananas - $2.50\n2. Whole Milk - $4.00\n3. Sourdough Bread - $5.00\n\nTotal: $11.50",
            has_attachments=False
        ))

        # Scenario 2: Marketing Email (Junk candidate)
        signals.append(EmailSignal(
            message_id="mock_msg_002",
            sender="newsletter@techstore.com",
            subject="Huge Sale on Laptops!",
            received_at=base_time - timedelta(hours=2),
            snippet="Save up to 50% this weekend only.",
            body_text="Don't miss our giant tech blowout. Click here.",
            has_attachments=True
        ))

        # Scenario 3: Another Receipt
        signals.append(EmailSignal(
            message_id="mock_msg_003",
            sender="receipts@grocer.com",
            subject="Order Confirmation",
            received_at=base_time - timedelta(days=1),
            snippet="Order confirmed. Delivering tomorrow.",
            body_text="Order #555.\nApples (1kg)\nEggs (12pk)",
            has_attachments=False
        ))

        return signals[:limit]
