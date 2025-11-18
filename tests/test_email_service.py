import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
from flask import Flask
from app.enums.directorate_codes import DirectorateCode
from app.infra.email_manager import EmailManager
from app.services.email_service import EmailService

# Garantir que o ambiente seja DEV para todos os testes
os.environ["ENV"] = "DEV"

class TestEmailService:
    def setup_method(self):
        # Criar uma aplicação Flask para os testes
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.template_folder = "tests/templates"  # Configurar um diretório de templates fictício
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Mock do conteúdo do template para evitar erro de arquivo ausente
        self.template_content = """
        <html>
            <body>
                <p>{{ Titulo }}</p>
                <p>{{ Descricao }}</p>
            </body>
        </html>
        """
        os.makedirs(self.app.template_folder, exist_ok=True)
        with open(f"{self.app.template_folder}/email-template.html", "w") as f:
            f.write(self.template_content)

    def teardown_method(self):
        # Remover o contexto da aplicação após os testes
        self.app_context.pop()
        # Remover o template fictício
        os.remove(f"{self.app.template_folder}/email-template.html")

    def test_send_email_with_template(self):
        sender = os.getenv("EMAIL_USER")
        base_url = os.getenv("BASE_URL")

        context = {
            "BASE_URL": base_url,
            "NIVEL": 2,
            "TITULO_POSTAGEM": "Pix fora do ar? Instabilidade atinge Itaú, BB e Nubank e gera milhares de reclamações nesta segunda (29)",
            "PERFIL_USUARIO": "Perfil Oficial",
            "AREAS_GESTORAS": "Ditec, Divar, UAC",
            "AREAS_INFORMADAS": "Relações com a Imprensa; Jurídico",
            "DESCRICAO_COMPLETA": (
                "De acordo com o portal O Globo, o sistema de transações instantâneas Pix apresenta instabilidades nesta segunda-feira..."
            ),
            "LINK_DUVIDAS": "https://einvestidor.estadao.com.br/ultimas/pix-fora-do-ar-hoje-bancos-itau-nubank-santander/",
            "EMAIL_CONTATO": "reputacao@bb.com.br",
            "EMAIL": "gk@gmail.com",
            "DIRECTORY": "BB"
        }

        subject = f"Alerta de Nível {context['NIVEL']} - {context['TITULO_POSTAGEM']}"

        email_manager = EmailManager()
        try:
            email_manager.send_email(sender, subject, self.template_content)
        except Exception as e:
            pytest.fail(f"Falha ao enviar e-mail: {e}")

    def test_send_email_with_bcc(self):
        sender = os.getenv("EMAIL_USER")
        recipients = ["recipient1@example.com"]
        cc = ["cc1@example.com"]
        bcc = ["bcc1@example.com", "bcc2@example.com"]
        subject = "Teste de envio com BCC"
        body = "<p>Este é um teste de envio de e-mail com BCC.</p>"

        email_manager = EmailManager()
        try:
            email_manager.send_email(recipients, subject, body, cc=cc, bcc=bcc)
        except Exception as e:
            pytest.fail(f"Falha ao enviar e-mail com BCC: {e}")

    def test_send_alert_to_directorates_with_bcc(self):
        email_service = EmailService()
        alert = MagicMock()
        alert.id = 1
        alert.title = "Teste de Alerta"
        alert.criticality_level.number = 3
        alert.is_repercussion = False
        alert.alert_text = "Texto de alerta para teste."  # Definir o atributo alert_text como string válida

        directorates = [DirectorateCode.FB, DirectorateCode.DIMAC_MARKETING_COM_PRIORITARIO]

        # Enviar o e-mail diretamente no ambiente DEV
        result = email_service.send_alert_to_directorates(alert, directorates)
        assert result["status"] == "sent", f"Falha ao enviar e-mail no ambiente DEV: {result.get('error')}"
        assert "to" in result and result["to"], "Lista de destinatários 'to' está vazia."
        assert "cc" in result and result["cc"], "Lista de destinatários 'cc' está vazia."
