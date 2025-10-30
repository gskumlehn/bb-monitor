class ErrorMessages:

    enum = {
        "DirectorateCode.invalid": "Diretoria inválida",
        "MailingStatus.invalid": "Status de envio inválido",
        "CriticalityLevel.invalid": "Nível de criticidade inválido",
        "AlertType.invalid": "Tipo de alerta inválido",
        "Stakeholders.invalid": "Stakeholder inválido",
    }

    model = {
        "Alert.missingFields": "Os seguintes campos obrigatórios estão ausentes ou vazios: {fields}",
        "Alert.mailingStatus.invalid": "Status de envio inválido",
        "Alert.criticalityLevel.invalid": "Nível de criticidade inválido",
        "Alert.alertTypes.invalid": "Tipo de alerta inválido",
        "Alert.stakeholders.invalid": "Stakeholder inválido",
        "Alert.urls.duplicate": "O alerta com a mesma lista de URLs já foi ingerido.",
        "Mailing.email.empty": "Email não pode ser vazio.",
        "Mailing.email.invalid": "Formato do email é inválido.",
        "Mailing.email.domain.invalid": "Domínio do email não é permitido",
    }
