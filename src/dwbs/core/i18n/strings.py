class LanguageResources:
    """
    D9.4 Language support (EN + HI)
    """

    STRINGS = {
        "EN": {
            "GREETING_MORNING": "Good morning!",
            "EXPIRY_SUMMARY_NONE": "You have no items expiring soon.",
            "EXPIRY_SUMMARY_ONE": "You have 1 item, {item}, expiring soon.",
            "EXPIRY_SUMMARY_MANY": "You have {count} items expiring soon, including {item}.",
            "COOK_SUGGESTION_INTRO": "You could cook",
            "OR": "or"
        },
        "HI": {
            "GREETING_MORNING": "Namaste!",
            "EXPIRY_SUMMARY_NONE": "Jaldi kharab hone wala koi saman nahi hai.",
            "EXPIRY_SUMMARY_ONE": "Aapka 1 item, {item}, jaldi kharab hone wala hai.",
            "EXPIRY_SUMMARY_MANY": "Aapke {count} items jaldi kharab hone wale hain, jaise ki {item}.",
            "COOK_SUGGESTION_INTRO": "Aap bana sakte hain",
            "OR": "ya"
        }
    }

    @classmethod
    def get_string(cls, lang: str, key: str, **kwargs) -> str:
        """
        Get localized string. Fallback to EN.
        """
        bundle = cls.STRINGS.get(lang.upper(), cls.STRINGS["EN"])
        template = bundle.get(key, cls.STRINGS["EN"].get(key, ""))

        if not template:
            return f"[{key}]"

        return template.format(**kwargs)
