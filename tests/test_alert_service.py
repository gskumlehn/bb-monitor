import unittest
from datetime import datetime, timedelta
from app.services.alert_service import AlertService
from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus
from app.enums.stakeholders import Stakeholders
from app.constants.error_messages import ErrorMessages
from app.enums.critical_topic import CriticalTopic
from app.enums.press_source import PressSource
from app.enums.social_media_source import SocialMediaSource
from app.enums.social_media_engagement import SocialMediaEngagement
from app.enums.repercussion import Repercussion
from zoneinfo import ZoneInfo
from app.models.alert import Alert

class TestAlertService(unittest.TestCase):
    def setUp(self):
        self.service = AlertService()

    def test_save_alert_success(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
            "critical_topic": [CriticalTopic.RELEVANT_POLITICAL_FIGURES],
            "press_sources": [PressSource.ONE_RELEVANT_VEHICLE],
            "social_media_sources": [SocialMediaSource.MICRO_INFLUENCER],
            "stakeholders": [Stakeholders.PRESS_JOURNALISTS],
            "social_media_engagements": [SocialMediaEngagement.INTERACTIONS_250],
            "history": "Test history",
        }

        saved_alert = self.service.save(alert_data)
        self.assertIsNotNone(saved_alert)

        db_alert = self.service.get_by_id(saved_alert.id)
        self.assertIsNotNone(db_alert)
        self.assertEqual(db_alert.title, alert_data["title"])
        self.assertEqual(db_alert.urls, alert_data["urls"])
        self.assertEqual(db_alert.delivery_datetime, alert_data["delivery_datetime"])
        self.assertEqual(db_alert.mailing_status, alert_data["mailing_status"])
        self.assertEqual(db_alert.criticality_level, alert_data["criticality_level"])
        self.assertEqual(db_alert.alert_types, alert_data["alert_types"])
        self.assertEqual(db_alert.profiles_or_portals, alert_data["profiles_or_portals"])
        self.assertEqual(db_alert.alert_text, alert_data["alert_text"])
        self.assertEqual(db_alert.critical_topic, alert_data["critical_topic"])
        self.assertEqual(db_alert.press_sources, alert_data["press_sources"])
        self.assertEqual(db_alert.social_media_sources, alert_data["social_media_sources"])
        self.assertEqual(db_alert.stakeholders, alert_data["stakeholders"])
        self.assertEqual(db_alert.social_media_engagements, alert_data["social_media_engagements"])
        self.assertEqual(db_alert.history, alert_data["history"])

        self.service.delete_by_id(saved_alert.id)

    def test_duplicate_urls(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
        }

        # Salva o primeiro alerta
        saved_alert = self.service.save(alert_data)
        self.assertIsNotNone(saved_alert)

        # Segunda inserção com URLs duplicadas deve levantar ValueError
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.duplicateUrls"])

        self.service.delete_by_id(saved_alert.id)

    def test_missing_required_fields(self):
        alert_data = {
            "title": "[[TESTE]] Test Alert",
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertIn("urls", str(context.exception))
        self.assertIn("delivery_datetime", str(context.exception))

    def test_invalid_mailing_status(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Test Alert",
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
            "title": "[[TESTE]] Test Alert",
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
            "title": "[[TESTE]] Test Alert",
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

    def test_invalid_critical_topic(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
            "critical_topic": ["INVALID_TOPIC"],  # Invalid critical topic
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.criticalTopic.invalid"])

    def test_invalid_press_sources(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
            "press_sources": ["INVALID_SOURCE"],  # Invalid press source
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.pressSources.invalid"])

    def test_invalid_social_media_sources(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
            "social_media_sources": ["INVALID_SOURCE"],  # Invalid social media source
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.socialMediaSources.invalid"])

    def test_invalid_social_media_engagements(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Test Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Test alert text",
            "social_media_engagements": ["INVALID_ENGAGEMENT"],  # Invalid social media engagement
        }
        with self.assertRaises(ValueError) as context:
            self.service.save(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.socialMediaEngagements.invalid"])

    def test_update_alert_success(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Original Title",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Original alert text",
            "critical_topic": [CriticalTopic.RELEVANT_POLITICAL_FIGURES],
            "press_sources": [PressSource.ONE_RELEVANT_VEHICLE],
            "social_media_sources": [SocialMediaSource.MICRO_INFLUENCER],
            "stakeholders": [Stakeholders.PRESS_JOURNALISTS],
            "social_media_engagements": [SocialMediaEngagement.INTERACTIONS_250],
            "history": "Original history",
        }

        # Save the initial alert
        saved_alert = self.service.save(alert_data)
        self.assertIsNotNone(saved_alert)

        # Update data (all fields except `urls` and `mailing_status`)
        update_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Updated Title",
            "delivery_datetime": datetime(2023, 11, 11, 11, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_2,
            "alert_types": [AlertType.SOCIAL_MEDIA],
            "profiles_or_portals": ["UpdatedProfile"],
            "alert_text": "Updated alert text",
            "critical_topic": [CriticalTopic.CORRUPTION_MONEY_LAUNDERING],
            "press_sources": [PressSource.GROUP_B],
            "social_media_sources": [SocialMediaSource.MACRO_INFLUENCER],  # Valid updated value
            "stakeholders": [Stakeholders.CLIENT_SOCIETY],
            "social_media_engagements": [SocialMediaEngagement.INTERACTIONS_2500],
            "history": "Updated history",
        }

        # Perform the update
        updated_alert = self.service.update(saved_alert.id, update_data)
        self.assertIsNotNone(updated_alert)

        # Fetch the updated alert from the database
        db_alert = self.service.get_by_id(saved_alert.id)
        self.assertIsNotNone(db_alert)

        # Assert that `urls` and `mailing_status` were not updated
        self.assertEqual(db_alert.urls, alert_data["urls"])
        self.assertEqual(db_alert.mailing_status, alert_data["mailing_status"])

        # Assert that other fields were updated
        self.assertEqual(db_alert.title, update_data["title"])
        self.assertEqual(db_alert.delivery_datetime, update_data["delivery_datetime"])
        self.assertEqual(db_alert.criticality_level, update_data["criticality_level"])
        self.assertEqual(db_alert.alert_types, update_data["alert_types"])
        self.assertEqual(db_alert.profiles_or_portals, update_data["profiles_or_portals"])
        self.assertEqual(db_alert.alert_text, update_data["alert_text"])
        self.assertEqual(db_alert.critical_topic, update_data["critical_topic"])
        self.assertEqual(db_alert.press_sources, update_data["press_sources"])
        self.assertEqual(db_alert.social_media_sources, update_data["social_media_sources"])
        self.assertEqual(db_alert.stakeholders, update_data["stakeholders"])
        self.assertEqual(db_alert.social_media_engagements, update_data["social_media_engagements"])
        self.assertEqual(db_alert.history, update_data["history"])

        # Clean up
        self.service.delete_by_id(saved_alert.id)

    def test_save_or_update_new_alert(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] New Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "New alert text",
            "critical_topic": [CriticalTopic.RELEVANT_POLITICAL_FIGURES],
            "press_sources": [PressSource.ONE_RELEVANT_VEHICLE],
            "social_media_sources": [SocialMediaSource.MICRO_INFLUENCER],
            "stakeholders": [Stakeholders.PRESS_JOURNALISTS],
            "social_media_engagements": [SocialMediaEngagement.INTERACTIONS_250],
            "history": "New history",
        }

        saved_alert = self.service.save_or_update(alert_data)
        self.assertIsNotNone(saved_alert)

        db_alert = self.service.get_by_id(saved_alert.id)
        self.assertIsNotNone(db_alert)
        self.assertEqual(db_alert.title, alert_data["title"])
        self.assertEqual(db_alert.urls, alert_data["urls"])

        self.service.delete_by_id(saved_alert.id)

    def test_save_or_update_existing_alert(self):
        alert_data = {
            "urls": ["http://example.com"],
            "title": "[[TESTE]] Original Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Original alert text",
            "critical_topic": [CriticalTopic.RELEVANT_POLITICAL_FIGURES],
            "press_sources": [PressSource.ONE_RELEVANT_VEHICLE],
            "social_media_sources": [SocialMediaSource.MICRO_INFLUENCER],
            "stakeholders": [Stakeholders.PRESS_JOURNALISTS],
            "social_media_engagements": [SocialMediaEngagement.INTERACTIONS_250],
            "history": "Original history",
        }

        saved_alert = self.service.save(alert_data)
        self.assertIsNotNone(saved_alert)

        update_data = {
            "urls": ["http://example.com"],  # Same URL to trigger update
            "title": "[[TESTE]] Updated Alert",
            "delivery_datetime": datetime(2023, 11, 11, 11, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,  # Should not change
            "criticality_level": CriticalityLevel.LEVEL_2,
            "alert_types": [AlertType.SOCIAL_MEDIA],
            "profiles_or_portals": ["UpdatedProfile"],
            "alert_text": "Updated alert text",
            "critical_topic": [CriticalTopic.CORRUPTION_MONEY_LAUNDERING],
            "press_sources": [PressSource.GROUP_B],
            "social_media_sources": [SocialMediaSource.MACRO_INFLUENCER],
            "stakeholders": [Stakeholders.CLIENT_SOCIETY],
            "social_media_engagements": [SocialMediaEngagement.INTERACTIONS_2500],
            "history": "Updated history",
        }

        updated_alert = self.service.save_or_update(update_data)
        self.assertIsNotNone(updated_alert)
        self.assertEqual(updated_alert.id, saved_alert.id)

        db_alert = self.service.get_by_id(updated_alert.id)
        self.assertIsNotNone(db_alert)
        self.assertEqual(db_alert.title, update_data["title"])
        self.assertEqual(db_alert.delivery_datetime, update_data["delivery_datetime"])
        self.assertEqual(db_alert.criticality_level, update_data["criticality_level"])
        self.assertEqual(db_alert.alert_types, update_data["alert_types"])
        self.assertEqual(db_alert.profiles_or_portals, update_data["profiles_or_portals"])
        self.assertEqual(db_alert.alert_text, update_data["alert_text"])
        self.assertEqual(db_alert.critical_topic, update_data["critical_topic"])
        self.assertEqual(db_alert.press_sources, update_data["press_sources"])
        self.assertEqual(db_alert.social_media_sources, update_data["social_media_sources"])
        self.assertEqual(db_alert.stakeholders, update_data["stakeholders"])
        self.assertEqual(db_alert.social_media_engagements, update_data["social_media_engagements"])
        self.assertEqual(db_alert.history, update_data["history"])

        # Assert that `urls` and `mailing_status` were not updated
        self.assertEqual(db_alert.urls, alert_data["urls"])
        self.assertEqual(db_alert.mailing_status, alert_data["mailing_status"])

        self.service.delete_by_id(saved_alert.id)

    def test_save_or_update_no_urls(self):
        alert_data = {
            "title": "[[TESTE]] Alert Without URLs",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Alert text without URLs",
        }

        with self.assertRaises(ValueError) as context:
            self.service.save_or_update(alert_data)
        self.assertIn("urls", str(context.exception))

    def test_save_alert_with_repercussion_success(self):
        # Create the original alert with a unique URL
        original_alert_data = {
            "urls": ["http://example.com/original-unique"],
            "title": "Original Alert",
            "delivery_datetime": datetime(2023, 10, 10, 10, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_1,
            "alert_types": [AlertType.PRESS],
            "profiles_or_portals": ["Profile1"],
            "alert_text": "Original alert text",
        }
        original_alert = self.service.save(original_alert_data)
        self.assertIsNotNone(original_alert)

        # Create the repercussion alert with a different unique URL
        repercussion_alert_data = {
            "urls": ["http://example.com/repercussion-unique"],
            "title": "Repercussion Alert",
            "delivery_datetime": datetime(2023, 10, 11, 11, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_2,
            "alert_types": [AlertType.SOCIAL_MEDIA],
            "profiles_or_portals": ["Profile2"],
            "alert_text": "Repercussion alert text",
            "previous_alert_id": original_alert.id,
        }
        repercussion_alert = self.service.save_or_update(repercussion_alert_data)
        self.assertIsNotNone(repercussion_alert)
        self.assertTrue(repercussion_alert.is_repercussion)
        self.assertIn(original_alert.id, repercussion_alert.previous_alerts_ids)

        # Clean up
        self.service.delete_by_id(repercussion_alert.id)
        self.service.delete_by_id(original_alert.id)

    def test_save_alert_with_nonexistent_previous_alert(self):
        # Attempt to create an alert with a non-existent previous alert ID
        non_existent_alert_id = "non-existent-id"
        alert_data = {
            "urls": ["http://example.com/repercussion"],
            "title": "Repercussion Alert",
            "delivery_datetime": datetime(2023, 10, 11, 11, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
            "mailing_status": MailingStatus.NOT_SENT,
            "criticality_level": CriticalityLevel.LEVEL_2,
            "alert_types": [AlertType.SOCIAL_MEDIA],
            "profiles_or_portals": ["Profile2"],
            "alert_text": "Repercussion alert text",
            "previous_alert_id": non_existent_alert_id,
        }

        with self.assertRaises(ValueError) as context:
            self.service.save_or_update(alert_data)
        self.assertEqual(str(context.exception), ErrorMessages.model["Alert.previousAlert.notFound"])


if __name__ == "__main__":
    unittest.main()
