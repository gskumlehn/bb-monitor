from typing import List
from app.constants.error_messages import ErrorMessages
from app.enums.directorate_codes import DirectorateCode
from app.enums.mailing_status import MailingStatus
from app.models.mailing_history import MailingHistory
from app.repositories.mailing_history_repository import MailingHistoryRepository
from app.services.alert_service import AlertService
from datetime import datetime

class MailingHistoryService:

    def save(self, history_data: dict) -> MailingHistory:
        self.validate_history_data(history_data)
        history = self.create(history_data)

        MailingHistoryRepository.save(history)

        alert = AlertService().get_by_id(history.alert_id)
        AlertService().update_mailing_status(alert, MailingStatus.MAILING_SENT)

        return MailingHistoryRepository.save(history)

    def validate_history_data(self, history_data: dict):
        required_fields = [
            "alert_id",
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

        for field in ["to_directorates", "cc_directorates", "bcc_directorates"]:
            if field in history_data and history_data[field]:
                for directorate in history_data[field]:
                    if not isinstance(directorate, DirectorateCode):
                        raise ValueError(ErrorMessages.model["MailingHistory.invalidDirectorate"])

    def create(self, history_data: dict) -> MailingHistory:
        history = MailingHistory()
        history.alert_id = history_data.get("alert_id")
        history.primary_directorate = history_data.get("primary_directorate")
        history.to_emails = history_data.get("to_emails", [])
        history.cc_emails = history_data.get("cc_emails", [])
        history.bcc_emails = history_data.get("bcc_emails", [])
        history.sender_email = history_data.get("sender_email")
        history.to_directorates = history_data.get("to_directorates", [])
        history.cc_directorates = history_data.get("cc_directorates", [])
        history.bcc_directorates = history_data.get("bcc_directorates", [])
        history.date_sent = datetime.utcnow()
        return history

    def delete_by_id(self, history_id: str):
        MailingHistoryRepository.delete_by_id(history_id)

    def list(self, alert_id: str) -> List[MailingHistory]:
        return MailingHistoryRepository.list(alert_id)

    def list_alerted_directorates(self, alert_id: str) -> List[DirectorateCode]:
        mailing_histories = self.list(alert_id)
        alerted_directorates = set()

        for history in mailing_histories:
            alerted_directorates.update(history.bcc_directorates)

        alerted_directorates = alerted_directorates.difference(DirectorateCode.exclusions())
        sorted_directorates = sorted(
            alerted_directorates, key=lambda d: d.value if hasattr(d, "value") else str(d)
        )
        return list(sorted_directorates)
