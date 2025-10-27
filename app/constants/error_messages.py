class ErrorMessages:

    enum = {
        "DirectorateCode.invalid": "Diretoria inválida",
        "MailingStatus.invalid": "Status de envio inválido",
        "CriticalityLevel.invalid": "Nível de criticidade inválido",
        "AlertType.invalid": "Tipo de alerta inválido",
        "InvolvedVariables.invalid": "Variável envolvida inválida",
        "Stakeholders.invalid": "Stakeholder inválido",
    }

    model = {
        "Alert.missingFields": "Os seguintes campos obrigatórios estão ausentes ou vazios: {fields}",
        "Alert.mailingStatusInvalid": "mailing_status deve ser um valor válido de MailingStatus, recebido: {value}",
        "Alert.criticalityLevelInvalid": "criticality_level deve ser um valor válido de CriticalityLevel, recebido: {value}",
        "Alert.alertTypesInvalid": "alert_types deve ser uma lista de valores válidos de AlertType, recebido: {value}",
        "Alert.involvedVariablesInvalid": "involved_variables deve ser uma lista de valores válidos de InvolvedVariables, recebido: {value}",
        "Alert.stakeholdersInvalid": "stakeholders deve ser uma lista de valores válidos de Stakeholders, recebido: {value}",
        "Alert.urlsDuplicate": "O alerta com a mesma lista de URLs já foi ingerido.",
        "Mailing.emailEmpty": "Email não pode ser vazio.",
        "Mailing.emailInvalid": "Formato do email é inválido.",
        "Mailing.emailDomainInvalid": "Domínio do email não é permitido",
    }
