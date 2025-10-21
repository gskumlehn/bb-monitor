from app.interfaces.enum_interface import EnumInterface

class MailingStatus(EnumInterface):
    NOT_SENT = "Não Enviado"
    SENT = "Enviado"
    EMAIL_SENT = "Email Enviado"
