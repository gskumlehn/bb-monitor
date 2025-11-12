from app.interfaces.enum_interface import EnumInterface

class MailingStatus(EnumInterface):

    NOT_SENT = "NÃO"
    SENT = "SIM"
    EMAIL_SENT = "Email Enviado"
    MAILING_SENT = "Mailing Enviado"