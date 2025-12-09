import os
from app.infra.smtp_manager import SMTPManager
from app.infra.ses_manager import SESManager

class EmailManager:
    def __init__(self):
        env = os.getenv("ENV", "").strip().upper()
        if env == "DEV":
            self.manager = SMTPManager()
        else:
            self.manager = SESManager()

    def send_email(self, recipients, subject, body, cc=None, bcc=None):
        return self.manager.send_email(recipients, subject, body, cc, bcc)
