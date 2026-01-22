import pytest
from datetime import date, timedelta
from decimal import Decimal
from src.dwbs.core.contracts.inventory import InventoryItem, ItemIdentity, Quantity, Unit
from src.dwbs.core.voice.generation.alert_generator import ExpiryAlertGenerator

class TestExpiryAlertGenerator:
    def setup_method(self):
        self.generator = ExpiryAlertGenerator()

    def create_item(self, days_offset: int) -> InventoryItem:
        return InventoryItem(
            item=ItemIdentity(name="Milk"),
            quantity=Quantity(value=Decimal(1), unit=Unit.LITER),
            expiry_date=date.today() + timedelta(days=days_offset)
        )

    def test_alert_today(self):
        item = self.create_item(0)
        alert = self.generator.generate_expiry_alert(item)
        assert alert == "Use your Milk by today."

    def test_alert_tomorrow(self):
        item = self.create_item(1)
        alert = self.generator.generate_expiry_alert(item)
        assert alert == "Use your Milk by tomorrow."

    def test_alert_expired(self):
        item = self.create_item(-1)
        alert = self.generator.generate_expiry_alert(item)
        assert alert == "Your Milk has expired."

    def test_no_alert_future(self):
        item = self.create_item(5)
        alert = self.generator.generate_expiry_alert(item)
        assert alert is None
