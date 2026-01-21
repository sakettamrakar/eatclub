import re
from typing import List, Optional
from decimal import Decimal
from ....contracts.failure import Result, ErrorCode
from ....contracts.inventory import Unit, Quantity, ItemIdentity
from ...draft.schema import DraftItem

class TextParser:
    """
    D7.3 PDF parser
    Extracts line items from text-based PDF content.
    """

    # Format: Name Quantity Unit (e.g., "Milk 2 L")
    # Strict regex: Start, Name (min 1 char), Space, Number, Space, Unit, End
    LINE_PATTERN = re.compile(r"^(?P<name>.+?)\s+(?P<qty>\d+(\.\d+)?)\s*(?P<unit>[a-zA-Z]+)$")

    def parse_text(self, text: str) -> Result[List[DraftItem]]:
        """
        Parses text content into a list of DraftItems.
        Expects one item per line.
        """
        if not text:
            return Result.fail(ErrorCode.MISSING_DATA, "Input text is empty")

        draft_items = []
        lines = text.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = self.LINE_PATTERN.match(line)
            if match:
                name = match.group("name").strip()
                qty_str = match.group("qty")
                unit_str = match.group("unit").upper()

                # Map unit
                try:
                    unit = self._map_unit(unit_str)
                except ValueError:
                    # If unit is invalid, we might treat it as part of name?
                    # But strict formatting says fail or skip.
                    # Task says: "Return partial/empty list with error flag" or "Extracts... from clean text"
                    # We will log or skip.
                    continue

                qty = Decimal(qty_str)

                draft_items.append(DraftItem(
                    item=ItemIdentity(name=name, confidence=1.0),
                    quantity=Quantity(value=qty, unit=unit)
                ))
            else:
                # If line doesn't match, maybe we skip it (header/footer junk)
                pass

        if not draft_items:
            return Result.fail(ErrorCode.MISSING_DATA, "No valid items found in text")

        return Result.success(draft_items)

    def _map_unit(self, unit_str: str) -> Unit:
        # Direct mapping to Enum values
        for unit in Unit:
            if unit.value == unit_str:
                return unit
        # Common aliases
        aliases = {
            "PCS": Unit.PIECE, "PC": Unit.PIECE, "PIECES": Unit.PIECE,
            "KG": Unit.KILOGRAM, "KGS": Unit.KILOGRAM,
            "G": Unit.GRAM, "GMS": Unit.GRAM,
            "L": Unit.LITER, "LITRE": Unit.LITER, "LITRES": Unit.LITER,
            "ML": Unit.MILLILITER,
            "PKT": Unit.PACKET, "PACK": Unit.PACKET
        }
        if unit_str in aliases:
            return aliases[unit_str]
        raise ValueError(f"Unknown unit: {unit_str}")
