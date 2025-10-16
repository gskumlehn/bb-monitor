import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"

class EmailService:
    def __init__(self, smtp_server=EMAIL_HOST, smtp_port=EMAIL_PORT, sender_email=EMAIL_USER, sender_password=EMAIL_PASS):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient, subject, body):
        message = MIMEMultipart("alternative")  # Define como multipart para suportar HTML
        message['From'] = self.sender_email
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))  # Anexa o corpo como HTML renderizado

        server = None
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if EMAIL_USE_TLS:
                server.starttls()
            server.login(self.sender_email, self.sender_password)  # Login após starttls
            server.send_message(message)
            print("E-mail enviado com sucesso!")
        except smtplib.SMTPServerDisconnected as e:
            print(f"Erro: Conexão com o servidor SMTP foi desconectada. Detalhes: {e}")
            raise
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            raise
        finally:
            if server:
                try:
                    server.quit()
                except smtplib.SMTPServerDisconnected:
                    print("Servidor já desconectado.")
