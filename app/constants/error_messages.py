class ErrorMessages:

    enum = {
        "DirectorateCode.invalid": "Diretoria inválida",
        "MailingStatus.invalid": "Status de envio inválido",
        "CriticalityLevel.invalid": "Nível de criticidade inválido",
        "AlertType.invalid": "Tipo de alerta inválido",
        "Stakeholders.invalid": "Stakeholder inválido",
        "CriticalTopic.invalid": "Tema crítico inválido",
        "PressSource.invalid": "Fonte de imprensa inválida",
        "SocialMediaSource.invalid": "Fonte de rede social inválida",
        "SocialMediaEngagement.invalid": "Engajamento de redes sociais inválido",
        "Repercussion.invalid": "Repercussão inválida",
    }

    model = {
        "Alert.missingFields": "Os seguintes campos obrigatórios estão ausentes ou vazios: {fields}",
        "Alert.mailingStatus.invalid": "Status de envio inválido",
        "Alert.criticalityLevel.invalid": "Nível de criticidade inválido",
        "Alert.alertTypes.invalid": "Tipo de alerta inválido",
        "Alert.stakeholders.invalid": "Stakeholder inválido",
        "Alert.duplicateUrls": "O alerta com a mesma lista de URLs já foi ingerido.",
        "Alert.criticalTopic.invalid": "Tema crítico inválido",
        "Alert.pressSources.invalid": "Fonte de imprensa inválida",
        "Alert.socialMediaSources.invalid": "Fonte de rede social inválida",
        "Alert.socialMediaEngagements.invalid": "Engajamento de redes sociais inválido",
        "Alert.repercussions.invalid": "Repercussão inválida",
        "Mailing.email.empty": "Email não pode ser vazio.",
        "Mailing.email.invalid": "Formato do email é inválido.",
        "Mailing.email.domain.invalid": "Domínio do email não é permitido",
    }
