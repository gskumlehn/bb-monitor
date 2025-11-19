import unittest
from datetime import datetime
from zoneinfo import ZoneInfo
from app.services.alert_service import AlertService
from app.services.mailing_history_service import MailingHistoryService
from app.enums.directorate_codes import DirectorateCode
from app.models.mailing_history import MailingHistory
from app.enums.mailing_status import MailingStatus
from app.enums.criticality_level import CriticalityLevel
from app.enums.alert_type import AlertType
from app.constants.error_messages import ErrorMessages

class TestMailingHistoryService(unittest.TestCase):
    def setUp(self):
        self.alert_service = AlertService()
        self.history_service = MailingHistoryService()

        # Create a test alert
        self.alert_data = {
            "urls": ["http://example.com"],
            "title": "Test Alert for Mailing History",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["TestProfile"],
            "alert_text": "Test alert text for mailing history",
        }
        self.alert = self.alert_service.save(self.alert_data)
        self.created_histories = []

    def tearDown(self):
        # Delete the test alert
        self.alert_service.delete_by_id(self.alert.id)

        # Delete all created mailing histories
        for history in self.created_histories:
            self.history_service.delete_by_id(history.id)  # Updated to use the new service method

    def test_save_mailing_history_success(self):
        history_data = {
            "alert_id": self.alert.id,
            "to_emails": ["recipient1@example.com", "recipient2@example.com"],
            "cc_emails": ["cc1@example.com", "cc2@example.com"],
            "bcc_emails": ["bcc1@example.com", "bcc2@example.com"],
            "sender_email": "sender@example.com",
            "to_directorates": [DirectorateCode.DIMAC_PRIORITARIO],
            "cc_directorates": [DirectorateCode.FB],
            "bcc_directorates": [DirectorateCode.FB, DirectorateCode.DIMAC_PRIORITARIO],
        }

        saved_history = self.history_service.save(history_data)
        self.assertIsNotNone(saved_history)
        self.assertEqual(saved_history.alert_id, history_data["alert_id"])
        self.assertEqual(saved_history.to_emails, history_data["to_emails"])
        self.assertEqual(saved_history.cc_emails, history_data["cc_emails"])
        self.assertEqual(saved_history.bcc_emails, history_data["bcc_emails"])
        self.assertEqual(saved_history.sender_email, history_data["sender_email"])
        self.assertEqual(saved_history.to_directorates, history_data["to_directorates"])
        self.assertEqual(saved_history.cc_directorates, history_data["cc_directorates"])
        self.assertEqual(saved_history.bcc_directorates, history_data["bcc_directorates"])

        # Validate that the alert's mailing status was updated
        updated_alert = self.alert_service.get_by_id(self.alert.id)
        self.assertIsNotNone(updated_alert)
        self.assertEqual(updated_alert.mailing_status, MailingStatus.MAILING_SENT)

        # Track created history for cleanup
        self.created_histories.append(saved_history)

    def test_missing_required_fields(self):
        history_data = {
            "alert_id": self.alert.id,
        }

        with self.assertRaises(ValueError) as context:
            self.history_service.save(history_data)
        self.assertIn("to_emails", str(context.exception))
        self.assertIn("sender_email", str(context.exception))

    def test_invalid_directorates(self):
        history_data = {
            "alert_id": self.alert.id,
            "to_emails": ["recipient1@example.com"],
            "cc_emails": ["cc1@example.com"],
            "bcc_emails": ["bcc1@example.com"],
            "sender_email": "sender@example.com",
            "to_directorates": ["INVALID_DIRECTORATE"],
        }

        with self.assertRaises(ValueError) as context:
            self.history_service.save(history_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["MailingHistory.invalidDirectorate"])

if __name__ == "__main__":
    unittest.main()
