import pytest
from dwbs.core.scoring.confidence import Confidence

def test_confidence_values():
    assert Confidence.manual_entry().score == 1.0
    assert Confidence.verified_ocr().score == 0.9
    assert Confidence.unverified_ocr().score == 0.4

def test_comparison():
    c1 = Confidence.manual_entry()
    c2 = Confidence.unverified_ocr()
    assert c2 < c1
    assert c1 > c2
    assert c1 == Confidence.manual_entry()
