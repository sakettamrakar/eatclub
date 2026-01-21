from pydantic import Field
from ..contracts import SystemContract

class Confidence(SystemContract):
    """
    D1.4 Confidence Scores
    Represents the reliability of an event or data point.
    """
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")

    @classmethod
    def manual_entry(cls) -> 'Confidence':
        """Explicit user action is the source of truth."""
        return cls(score=1.0)

    @classmethod
    def verified_ocr(cls) -> 'Confidence':
        """OCR detection confirmed by user."""
        return cls(score=0.9)

    @classmethod
    def unverified_ocr(cls) -> 'Confidence':
        """Raw OCR output, potentially noisy."""
        return cls(score=0.4)

    def __lt__(self, other):
        if not isinstance(other, Confidence):
            return NotImplemented
        return self.score < other.score

    def __eq__(self, other):
        if not isinstance(other, Confidence):
            return NotImplemented
        return self.score == other.score
