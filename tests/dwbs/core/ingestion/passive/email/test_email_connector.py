import pytest
from dwbs.core.ingestion.passive.email.connector import MockGmailConnector
from dwbs.core.ingestion.passive.email.types import EmailSignal

def test_mock_connector_connection():
    connector = MockGmailConnector()
    assert connector.connect() is True

def test_mock_connector_fetch_signals():
    connector = MockGmailConnector()
    signals = connector.fetch_signals(label="INBOX", limit=2)

    assert len(signals) == 2
    assert isinstance(signals[0], EmailSignal)

    # Verify first signal (Receipt)
    assert signals[0].message_id == "mock_msg_001"
    assert signals[0].sender == "orders@freshmarket.com"
    assert "Fresh Market" in signals[0].body_text

    # Verify second signal (Junk)
    assert signals[1].message_id == "mock_msg_002"
    assert signals[1].has_attachments is True

def test_mock_connector_limit():
    connector = MockGmailConnector()
    signals = connector.fetch_signals(label="INBOX", limit=1)
    assert len(signals) == 1
    assert signals[0].message_id == "mock_msg_001"
