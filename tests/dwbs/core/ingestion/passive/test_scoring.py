import pytest
from decimal import Decimal
from src.dwbs.core.contracts.inventory import Unit, Quantity, ItemIdentity
from src.dwbs.core.ingestion.draft.schema import DraftItem
from src.dwbs.core.ingestion.passive.scoring.scorer import ConfidenceScorer

class TestConfidenceScorer:
    def setup_method(self):
        self.scorer = ConfidenceScorer()

    def create_draft_items(self):
        return [
            DraftItem(
                item=ItemIdentity(name="Milk", confidence=1.0), # Default 1.0 from parser
                quantity=Quantity(value=Decimal("1"), unit=Unit.LITER)
            )
        ]

    def test_score_known_vendor(self):
        items = self.create_draft_items()
        scored = self.scorer.score_drafts(items, "orders@grocery.com")

        assert len(scored) == 1
        assert scored[0].item.confidence == 0.9

    def test_score_unknown_vendor(self):
        items = self.create_draft_items()
        scored = self.scorer.score_drafts(items, "random@stranger.com")

        assert len(scored) == 1
        assert scored[0].item.confidence == 0.3

    def test_score_missing_sender(self):
        items = self.create_draft_items()
        scored = self.scorer.score_drafts(items, "")

        assert len(scored) == 1
        assert scored[0].item.confidence == 0.1

    def test_score_domain_match(self):
        items = self.create_draft_items()
        scored = self.scorer.score_drafts(items, "receipts@amazon.com")

        assert len(scored) == 1
        assert scored[0].item.confidence == 0.9
