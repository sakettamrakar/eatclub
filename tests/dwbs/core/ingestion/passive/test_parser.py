import pytest
from decimal import Decimal
from src.dwbs.core.contracts.inventory import Unit
from src.dwbs.core.ingestion.passive.parser.parser import TextParser

class TestTextParser:
    def setup_method(self):
        self.parser = TextParser()

    def test_parse_valid_lines(self):
        text = """
        Milk 1 L
        Eggs 12 PCS
        Rice 5 KG
        """
        result = self.parser.parse_text(text)
        assert result.is_success
        items = result.value
        assert len(items) == 3

        assert items[0].item.name == "Milk"
        assert items[0].quantity.value == Decimal("1")
        assert items[0].quantity.unit == Unit.LITER

        assert items[1].item.name == "Eggs"
        assert items[1].quantity.value == Decimal("12")
        assert items[1].quantity.unit == Unit.PIECE

        assert items[2].item.name == "Rice"
        assert items[2].quantity.value == Decimal("5")
        assert items[2].quantity.unit == Unit.KILOGRAM

    def test_parse_mixed_content(self):
        text = """
        Invoice #123
        Date: 2023-01-01

        Tomatoes 500 G
        Bread 1 PKT

        Total: $10.00
        """
        result = self.parser.parse_text(text)
        assert result.is_success
        items = result.value
        assert len(items) == 2

        assert items[0].item.name == "Tomatoes"
        assert items[0].quantity.value == Decimal("500")
        assert items[0].quantity.unit == Unit.GRAM

        assert items[1].item.name == "Bread"
        assert items[1].quantity.unit == Unit.PACKET

    def test_parse_empty(self):
        result = self.parser.parse_text("")
        assert result.is_failure

    def test_parse_no_matches(self):
        text = "Just some random text\nNo items here"
        result = self.parser.parse_text(text)
        assert result.is_failure
