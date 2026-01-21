from typing import List
import re
from ..email.types import EmailSignal
from .types import InvoiceType
from ....contracts.failure import Result, ErrorCode

class InvoiceClassifier:
    """
    D7.2 Invoice classification
    Rule-based keyword classifier to identify "Grocery Invoice" vs "Junk".
    """

    GROCERY_KEYWORDS = {
        r"\breceipt\b", r"\border\b", r"\binvoice\b",
        r"\bgrocery\b", r"\bsupermarket\b", r"\bmart\b", r"\bfresh\b", r"\bmarket\b", r"\bdelivery\b"
    }

    JUNK_KEYWORDS = {
        r"\bnewsletter\b", r"\balert\b", r"\bpromotion\b", r"\bsale\b", r"\boffer\b",
        r"\bmarketing\b", r"\bweekly ad\b", r"\bsecurity alert\b"
    }

    def classify_email(self, signal: EmailSignal) -> Result[InvoiceType]:
        """
        Classifies an email signal based on subject and sender.
        """
        if not signal:
             return Result.fail(ErrorCode.MISSING_DATA, "Signal is None")

        text_content = (signal.subject + " " + (signal.sender or "")).lower()

        # Check for Grocery keywords
        for pattern in self.GROCERY_KEYWORDS:
            if re.search(pattern, text_content):
                return Result.success(InvoiceType.GROCERY_INVOICE)

        # Check for Junk keywords
        for pattern in self.JUNK_KEYWORDS:
             if re.search(pattern, text_content):
                return Result.success(InvoiceType.JUNK)

        # Default to Unknown if ambiguous
        return Result.success(InvoiceType.UNKNOWN)
