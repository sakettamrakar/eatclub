import pytest
from decimal import Decimal
from datetime import date
from src.dwbs.core.contracts.inventory import InventoryItem, ItemIdentity, Quantity, Unit, StockStatus
from src.dwbs.core.voice.generation.summary_generator import DailySummaryGenerator

class TestDailySummaryGenerator:
    def setup_method(self):
        self.generator = DailySummaryGenerator()

    def test_summary_no_items(self):
        script = self.generator.generate_daily_summary([])
        assert "no items expiring" in script

    def test_summary_one_item(self):
        item = InventoryItem(
            item=ItemIdentity(name="Milk"),
            quantity=Quantity(value=Decimal(1), unit=Unit.LITER),
            expiry_date=date.today()
        )
        script = self.generator.generate_daily_summary([item])
        assert "1 item, Milk" in script

    def test_summary_multiple_items(self):
        item1 = InventoryItem(
            item=ItemIdentity(name="Milk"),
            quantity=Quantity(value=Decimal(1), unit=Unit.LITER)
        )
        item2 = InventoryItem(
            item=ItemIdentity(name="Bread"),
            quantity=Quantity(value=Decimal(1), unit=Unit.PACKET)
        )
        script = self.generator.generate_daily_summary([item1, item2])
        assert "2 items expiring soon" in script
        assert "including Milk" in script
