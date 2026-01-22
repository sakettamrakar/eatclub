import pytest
from src.dwbs.core.i18n.strings import LanguageResources

class TestLanguageResources:

    def test_english_default(self):
        s = LanguageResources.get_string("EN", "GREETING_MORNING")
        assert s == "Good morning!"

    def test_hindi_lookup(self):
        s = LanguageResources.get_string("HI", "GREETING_MORNING")
        assert s == "Namaste!"

    def test_fallback_to_english(self):
        # If language not found
        s = LanguageResources.get_string("FR", "GREETING_MORNING")
        assert s == "Good morning!"

    def test_formatting(self):
        s = LanguageResources.get_string("EN", "EXPIRY_SUMMARY_ONE", item="Milk")
        assert s == "You have 1 item, Milk, expiring soon."

        s_hi = LanguageResources.get_string("HI", "EXPIRY_SUMMARY_ONE", item="Milk")
        assert s_hi == "Aapka 1 item, Milk, jaldi kharab hone wala hai."
