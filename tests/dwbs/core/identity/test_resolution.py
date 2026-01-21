import pytest
from dwbs.core.identity.resolution import ItemIdentity

def test_identity_equality():
    item1 = ItemIdentity(name="Tomato", variant="Fresh")
    item2 = ItemIdentity(name="Tomato", variant="Fresh")
    item3 = ItemIdentity(name="Tomato", variant="Canned")
    item4 = ItemIdentity(name="Tomato", variant="Fresh", brand="Heinz")

    assert item1 == item2
    assert item1 != item3
    assert item1 != item4

    # Verify hash for map usage
    s = {item1}
    assert item2 in s
    assert item3 not in s

def test_full_name():
    item = ItemIdentity(name="Tomato", variant="Fresh", brand="Heinz")
    assert item.full_name() == "Tomato (Fresh) [Heinz]"
