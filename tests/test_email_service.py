import os
import pytest
from app.services.email_service import EmailService
from dotenv import load_dotenv

def test_send_email_with_template():
    load_dotenv()

    sender = os.getenv("EMAIL_USER")
    base_url = os.getenv("BASE_URL")
    assert sender is not None, "EMAIL_USER não está definido no .env"
    assert base_url is not None, "BASE_URL não está definido no .env"

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
        "VARIAVEIS_ENVOLVIDAS": "".join(
            f"<li>{var}</li>" for var in [
                "Pix", "instabilidade", "Banco Central", "Downdetector",
                "bancos brasileiros", "C6 Bank", "Itaú", "Bradesco", "Santander", "Inter"
            ]
        ),
        "STAKEHOLDERS": "Clientes; Imprensa; Reguladores",
        "LINK_DUVIDAS": "https://einvestidor.estadao.com.br/ultimas/pix-fora-do-ar-hoje-bancos-itau-nubank-santander/",
        "EMAIL_CONTATO": "reputacao@bb.com.br",
        "EMAIL": "gk@gmail.com",
        "DIRECTORY": "BB"
    }

    template_path = "../app/templates/email-template.html"
    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    for key, value in context.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))

    # Verifica se o link no rodapé foi gerado corretamente
    expected_remove_link = f"{context['BASE_URL']}/mailing/remove-ui?email={context['EMAIL']}&directorate_code={context['DIRECTORY']}"
    assert expected_remove_link in template, "O link de remoção no rodapé não foi gerado corretamente."

    subject = f"Alerta de Nível {context['NIVEL']} - {context['TITULO_POSTAGEM']}"

    email_service = EmailService()
    try:
        email_service.send_email(sender, subject, template)
    except Exception as e:
        pytest.fail(f"Falha ao enviar e-mail: {e}")
