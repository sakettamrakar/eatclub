from datetime import datetime
from typing import Optional
from pydantic import Field
from ....contracts.base import SystemContract

class EmailSignal(SystemContract):
    """
    D7.1 Email Connector
    Represents the metadata and content extracted from an email source.
    Acts as the raw signal for downstream classification and parsing.
    """
    message_id: str = Field(..., description="Unique ID from the email provider")
    sender: str = Field(..., description="Sender address or name")
    subject: str = Field(..., description="Subject line of the email")
    received_at: datetime = Field(..., description="Date and time the email was received")
    snippet: Optional[str] = Field(None, description="Short snippet/preview of the email")
    body_text: Optional[str] = Field(None, description="Extracted plain text body content")
    has_attachments: bool = Field(False, description="Whether the email has attachments")
