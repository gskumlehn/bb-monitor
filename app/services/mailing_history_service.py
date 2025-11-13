from app.constants.error_messages import ErrorMessages
from app.enums.directorate_codes import DirectorateCode
from app.models.mailing_history import MailingHistory
from app.repositories.mailing_history_repository import MailingHistoryRepository
from datetime import datetime

class MailingHistoryService:
    def save(self, history_data: dict) -> MailingHistory:
        self.validate_history_data(history_data)
        history = self.create(history_data)
        return MailingHistoryRepository.save(history)

    def validate_history_data(self, history_data: dict):
        required_fields = [
            "alert_id",
            "primary_directorate",
            "to_emails",
            "sender_email",
        ]

        missing_fields = [
            field
            for field in required_fields
            if field not in history_data or not history_data[field]
        ]
        if missing_fields:
            raise ValueError(
                ErrorMessages.model["MailingHistory.missingFields"].format(
                    fields=", ".join(missing_fields)
                )
            )

        if not isinstance(history_data.get("primary_directorate"), DirectorateCode):
            raise ValueError(ErrorMessages.model["MailingHistory.primaryDirectorate.invalid"])

    def create(self, history_data: dict) -> MailingHistory:
        history = MailingHistory()
        history.alert_id = history_data.get("alert_id")
        history.primary_directorate = history_data.get("primary_directorate")
        history.to_emails = history_data.get("to_emails", [])
        history.cc_emails = history_data.get("cc_emails", [])
        history.sender_email = history_data.get("sender_email")
        history.date_sent = datetime.utcnow()
        return history
