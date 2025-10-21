import unittest
from app.services.mailing_service import MailingService
from app.enums.directorate_codes import DirectorateCode
from app.constants.error_messages import ErrorMessages

class TestMailingService(unittest.TestCase):
    def setUp(self):
        self.service = MailingService()

    def test_create_without_email(self):
        with self.assertRaises(ValueError) as context:
            self.service.save("", DirectorateCode.FB)
        self.assertEqual(str(context.exception), ErrorMessages.model["Mailing.email.empty"])

    def test_create_without_directorate_code(self):
        with self.assertRaises(ValueError) as context:
            self.service.save("test@futurebrand.com", "")
        self.assertEqual(str(context.exception), ErrorMessages.enum["DirectorateCode.invalid"])

    def test_create_with_invalid_email(self):
        with self.assertRaises(ValueError) as context:
            self.service.save("invalid-email", DirectorateCode.FB.name)
        self.assertEqual(str(context.exception), ErrorMessages.model["Mailing.email.invalid"])

    def test_create_with_disallowed_domain(self):
        with self.assertRaises(ValueError) as context:
            self.service.save("test@notallowed.com", DirectorateCode.FB.name)
        self.assertEqual(
            str(context.exception),
            ErrorMessages.model["Mailing.email.domain.invalid"]
        )

    def test_duplicate_insert_and_delete(self):
        email = "test@futurebrand.com"
        code = DirectorateCode.FB.name

        try:
            self.service.save(email, code)
        except Exception as e:
            self.fail(f"save() raised an exception unexpectedly: {e}")

        try:
            self.service.save(email, code)
        except Exception as e:
            self.fail(f"save() raised an exception unexpectedly on duplicate insert: {e}")

        try:
            self.service.delete(email, code)
        except Exception as e:
            self.fail(f"delete() raised an exception unexpectedly: {e}")

if __name__ == "__main__":
    unittest.main()
