from enum import Enum

class InvoiceType(str, Enum):
    GROCERY_INVOICE = "GROCERY_INVOICE"
    JUNK = "JUNK"
    UNKNOWN = "UNKNOWN"
