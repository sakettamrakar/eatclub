import pytest
from datetime import date, timedelta
from dwbs.core.expiry.calculator import ExpiryCalculator
from dwbs.core.identity.resolution import ItemIdentity

def test_known_item_expiry():
    item = ItemIdentity(name="Tomato")
    p_date = date(2023, 1, 1)
    expiry = ExpiryCalculator.predict_expiry(item, p_date)
    assert expiry == p_date + timedelta(days=7)

def test_unknown_item_expiry():
    item = ItemIdentity(name="ExoticFruit")
    p_date = date(2023, 1, 1)
    expiry = ExpiryCalculator.predict_expiry(item, p_date)
    # Default is 3
    assert expiry == p_date + timedelta(days=3)
