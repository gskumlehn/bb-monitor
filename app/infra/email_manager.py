from app.infra.environment import Environment
from app.infra.smtp_manager import SMTPManager
from app.infra.ses_manager import SESManager

class EmailManager:
    def __init__(self):
        if Environment.is_development():
            self.manager = SMTPManager()
        else:
            self.manager = SESManager()

    def send_email(self, recipients, subject, body, cc=None, bcc=None):
        return self.manager.send_email(recipients, subject, body, cc, bcc)
