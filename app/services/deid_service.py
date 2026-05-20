import uuid

from sqlalchemy.orm import Session

from app.models.token_map import PIITokenMap
from app.models.audit_log import PIIAuditLog
from app.utils.pii_detector import detect_pii


class DeIdentificationService:

    def __init__(self, db: Session):
        self.db = db

    def generate_token(self, value, pii_type):

        existing = (
            self.db.query(PIITokenMap)
            .filter_by(real_value=value)
            .first()
        )

        if existing:
            return existing.token

        token = f"{pii_type.upper()}_{uuid.uuid4().hex[:8]}"

        new_entry = PIITokenMap(
            token=token,
            real_value=value,
            pii_type=pii_type
        )

        self.db.add(new_entry)

        audit = PIIAuditLog(
            field_name=pii_type,
            masked_value=token
        )

        self.db.add(audit)

        self.db.commit()

        return token

    def sanitize(self, data):

        if isinstance(data, dict):

            sanitized = {}

            for key, value in data.items():

                pii_type = detect_pii(key, value)

                if pii_type:
                    sanitized[key] = self.generate_token(
                        value,
                        pii_type
                    )

                else:
                    sanitized[key] = self.sanitize(value)

            return sanitized

        elif isinstance(data, list):

            return [self.sanitize(item) for item in data]

        return data
