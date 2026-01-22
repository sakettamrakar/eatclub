import logging
from datetime import datetime
from pydantic import Field
from ....contracts.base import SystemContract

# Configure dedicated logger for audit
audit_logger = logging.getLogger("dwbs.audit.ingest")
audit_logger.setLevel(logging.INFO)
# In a real app, this would be configured to write to a secure file or service

class IngestAuditLog(SystemContract):
    timestamp: datetime
    event_type: str
    source_reference: str
    outcome: str
    details: str

class IngestAuditLogger:
    """
    D7 Email & PDF Ingestion (Hardening)
    """

    def log_draft_created(self, source_id: str, draft_count: int):
        entry = IngestAuditLog(
            timestamp=datetime.now(),
            event_type="DRAFT_CREATED",
            source_reference=source_id,
            outcome="SUCCESS",
            details=f"Created {draft_count} draft items"
        )
        self._write_log(entry)

    def log_draft_rejected(self, source_id: str, reason: str):
        entry = IngestAuditLog(
            timestamp=datetime.now(),
            event_type="DRAFT_REJECTED",
            source_reference=source_id,
            outcome="FAILURE",
            details=reason
        )
        self._write_log(entry)

    def _write_log(self, entry: IngestAuditLog):
        # Format: [TIMESTAMP] [EVENT] [SOURCE] [OUTCOME] - DETAILS
        log_msg = f"[{entry.timestamp.isoformat()}] [{entry.event_type}] [{entry.source_reference}] [{entry.outcome}] - {entry.details}"
        audit_logger.info(log_msg)
