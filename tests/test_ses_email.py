import os
import unittest
from dotenv import load_dotenv
from app.infra.ses_manager import SESManager

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class TestSESManagerIntegration(unittest.TestCase):

    def setUp(self):
        """Configura o teste, garantindo que as variáveis de ambiente necessárias estão presentes."""
        self.sender_email = os.getenv("SES_SENDER_EMAIL")
        self.recipient_email = "gkumlehn@futurebrand.com.br"


        if not all([
            os.getenv("AWS_ACCESS_KEY_ID"),
            os.getenv("AWS_SECRET_ACCESS_KEY"),
            os.getenv("AWS_REGION"),
            self.sender_email,
            self.recipient_email
        ]):
            self.fail("Required environment variables for integration test are not set.")

        # Instancia o SESManager, que irá carregar as credenciais do ambiente
        self.ses_manager = SESManager()

    def test_send_real_email(self):
        """
        Tenta enviar um e-mail real usando as credenciais do .env.
        Verifica se o SES aceitou o e-mail retornando um MessageId.
        """
        # Arrange
        subject = "SES Integration Test"
        body = "<h1>This is a real test email</h1><p>Sent from the integration test.</p>"

        # Act
        print(f"Sending real test email from {self.sender_email} to {self.recipient_email}...")
        try:
            message_id = self.ses_manager.send_email(
                recipients=[self.recipient_email],
                subject=subject,
                body=body
            )
        except Exception as e:
            self.fail(f"SESManager.send_email raised an exception unexpectedly: {e}")

        # Assert
        self.assertIsInstance(message_id, str)
        self.assertGreater(len(message_id), 0)
        print(f"Test email sent successfully. MessageId: {message_id}")

if __name__ == '__main__':
    unittest.main()
