import unittest
from datetime import datetime
from app.services.alert_service import AlertService
from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus
from app.enums.stakeholders import Stakeholders
from app.constants.error_messages import ErrorMessages

class TestAlertService(unittest.TestCase):
    def setUp(self):
        self.service = AlertService()

    def test_save_alert_success(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
        }

        saved_alert = self.service.save(alert_data)
        self.assertIsNotNone(saved_alert)

        db_alert = self.service.get_by_id(saved_alert.id)
        self.assertIsNotNone(db_alert)
        self.assertEqual(db_alert.title, alert_data["title"])

        second_saved = self.service.save(alert_data)
        self.assertIsNotNone(second_saved)
        self.assertEqual(second_saved.id, saved_alert.id)

        self.service.delete_by_id(saved_alert.id)

    def test_duplicate_urls(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
        }

        # Salva o primeiro alerta
        saved_alert = self.service.save(alert_data)

        # Segunda inserção deve retornar o mesmo alerta (early return)
        second_saved = self.service.save(alert_data)
        self.assertIsNotNone(second_saved)
        self.assertEqual(second_saved.id, saved_alert.id)

        self.service.delete_by_id(saved_alert.id)

    def test_missing_required_fields(self):
        alert_data = {
            "title": "Test Alert",
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertIn("urls", str(context.exception))
        self.assertIn("delivery_datetime", str(context.exception))

    def test_invalid_mailing_status(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": "INVALID_STATUS",  # Invalid mailing status
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.mailingStatus.invalid"])

    def test_invalid_criticality_level(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": "INVALID_LEVEL",  # Invalid criticality level
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.criticalityLevel.invalid"])

    def test_invalid_alert_types(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": ["INVALID_TYPE"],  # Invalid alert type
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.alertTypes.invalid"])

    def test_invalid_involved_variables(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
            "involved_variables": ["INVALID_VARIABLE"],  # Invalid involved variable
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.involvedVariables.invalid"])

    def test_invalid_stakeholders(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
            "stakeholders": ["INVALID_STAKEHOLDER"],  # Invalid stakeholder
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.stakeholders.invalid"])

if __name__ == "__main__":
    unittest.main()
