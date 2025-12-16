import os
import boto3
import time
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
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

        all_unique_targets = set(to_list + cc_list + bcc_list)

        if not all_unique_targets:
            print("Erro: Nenhum destinatário definido.")
            return []

        header_to = ", ".join(to_list)
        header_cc = ", ".join(cc_list)
        reply_to_emails = to_list + cc_list
        header_reply_to = ", ".join(reply_to_emails)

        sent_ids = []

        print(f"Iniciando envio para {len(all_unique_targets)} destinatários únicos...")

        for target_email in all_unique_targets:
            try:
                message = MIMEMultipart("alternative")
                message['From'] = self.sender_email
                if header_to:
                    message['To'] = header_to
                if header_cc:
                    message['Cc'] = header_cc
                if header_reply_to:
                    message.add_header('Reply-To', header_reply_to)
                message['Subject'] = subject
                message.attach(MIMEText(body, 'html'))

                response = self.client.send_raw_email(
                    Source=self.sender_email,
                    Destinations=[target_email],
                    RawMessage={
                        'Data': message.as_string(),
                    }
                )

                sent_ids.append(response['MessageId'])
                time.sleep(0.1)

            except ClientError as e:
                print(f"Erro ao enviar para {target_email}: {e.response['Error']['Message']}")
                if e.response['Error']['Code'] == 'Throttling':
                    print("Atingido limite de envios por segundo. Aguardando...")
                    time.sleep(1)
            except Exception as e:
                print(f"Erro inesperado para {target_email}: {e}")

        print(f"Processo finalizado. {len(sent_ids)} e-mails enviados com sucesso.")
        return sent_ids
