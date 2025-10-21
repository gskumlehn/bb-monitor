class ErrorMessages:
    enum = {
        "DirectorateCode.invalid": "Diretoria inválida",
        "MailingStatus.invalid": "Status de envio inválido",
        "CriticalityLevel.invalid": "Nível de criticidade inválido",
    }

    model = {
        "Mailing.email.empty": "Email não pode ser vazio.",
        "Mailing.email.invalid": "Formato do email é inválido.",
        "Mailing.email.domain.invalid": "Domínio do email não é permitido",
    }
