import os
import boto3
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SES_SENDER_EMAIL = os.getenv("SES_SENDER_EMAIL")

class SESManager:

    def __init__(self, aws_access_key=AWS_ACCESS_KEY_ID, aws_secret_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION,
                 sender_email=SES_SENDER_EMAIL):
        self.sender_email = sender_email
        self.client = boto3.client(
            'ses',
            region_name=region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )

    def send_email(self, recipients, subject, body, cc=None, bcc=None):
        # --- Lógica de tratamento de listas (Idêntica à original) ---
        if isinstance(recipients, str):
            to_list = [r.strip() for r in recipients.split(",") if r.strip()]
        else:
            to_list = list(recipients or [])

        if isinstance(cc, str):
            cc_list = [r.strip() for r in cc.split(",") if r.strip()]
        else:
            cc_list = list(cc or [])

        if isinstance(bcc, str):
            bcc_list = [r.strip() for r in bcc.split(",") if r.strip()]
        else:
            bcc_list = list(bcc or [])

        # Lista combinada para o envelope de envio da AWS (quem realmente recebe)
        all_recipients = to_list + cc_list + bcc_list

        if not all_recipients:
            print("Erro: Nenhum destinatário definido.")
            return

        # --- Construção do MIME (Idêntica à original) ---
        message = MIMEMultipart("alternative")
        message['From'] = self.sender_email
        message['To'] = ", ".join(to_list)
        if cc_list:
            message['Cc'] = ", ".join(cc_list)
        # Nota: Não adicionamos header de BCC no MIME para não expor os e-mails ocultos,
        # mas eles devem estar em 'all_recipients' para o SES entregar.

        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))

        # --- Envio via Boto3 (Substituindo smtplib) ---
        try:
            # send_raw_email é necessário quando usamos objetos MIME/Multipart
            response = self.client.send_raw_email(
                Source=self.sender_email,
                Destinations=all_recipients,  # O SES usa essa lista para rotear, não os headers do MIME
                RawMessage={
                    'Data': message.as_string(),
                }
            )
            print(f"E-mail enviado com sucesso! MessageId: {response['MessageId']}")
            return response['MessageId']

        except ClientError as e:
            print(f"Erro ao enviar e-mail via SES: {e.response['Error']['Message']}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise