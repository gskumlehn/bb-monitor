from app.enums.mention_category_name import MentionCategoryName
from app.enums.directorate_codes import DirectorateCode

class MailingConstants:
    ALLOWED_DOMAINS = {
        "futurebrand.com",
        "futurebrand.com.br",
        "bb.com.br"
    }

    CATEGORY_TO_DIRECTORATE_MAP = {
        MentionCategoryName.ESG_HARASSMENT_OR_PAY_INEQUITY: [
            DirectorateCode.ASG,
            DirectorateCode.DIPES
        ],
        MentionCategoryName.ESG_HUMAN_RIGHTS_AND_DIVERSITY: [
            DirectorateCode.ASG
        ],
        MentionCategoryName.AGRIBUSINESS_SUSTAINABILITY_IN_AGRO: [
            DirectorateCode.DIRAG,
            DirectorateCode.ASG
        ],
        MentionCategoryName.AGRIBUSINESS_PROGRAMS_FOR_AGRO: [
            DirectorateCode.DIRAG,
            DirectorateCode.DIGOV
        ],
        MentionCategoryName.AGRIBUSINESS_GENERAL_AGRO_OPERATIONS: [
            DirectorateCode.DIRAG
        ],
        MentionCategoryName.RELATED_ENTITIES_BB_ASSET: [
            DirectorateCode.BB_ASSET,
            DirectorateCode.UPE
        ],
        MentionCategoryName.RELATED_ENTITIES_SECURITIES: [
            DirectorateCode.BB_SEGUROS,
            DirectorateCode.UPE
        ],
        MentionCategoryName.RELATED_ENTITIES_BB_CONSORTIUM: [
            DirectorateCode.UPE,
            DirectorateCode.BB_CONSORCIOS
        ],
        MentionCategoryName.RELATED_ENTITIES_GENERAL_COLLABORATES: [
            DirectorateCode.UPE
        ],
        MentionCategoryName.STRATEGY_CORPORATE_POLICIES: [
            DirectorateCode.DIREO
        ],
        MentionCategoryName.STRATEGY_AGENCY_GOALS_AND_BUSINESS: [
            DirectorateCode.DIVAR
        ],
        MentionCategoryName.FINANCE_ACCOUNTING_AND_TREASURY: [
            DirectorateCode.DIFIN,
            DirectorateCode.URI,
            DirectorateCode.UCI,
            DirectorateCode.TESOURARIA_GLOBAL,
            DirectorateCode.COGER
        ],
        MentionCategoryName.SUPPLIER_GENERAL: [
            DirectorateCode.DISEC
        ],
        MentionCategoryName.GOVERNANCE_COMPLIANCE: [
            DirectorateCode.DICOI,
            DirectorateCode.DITEC
        ],
        MentionCategoryName.GOVERNANCE_FEDERAL_RESOURCE_PROGRAM: [
            DirectorateCode.DIGOV,
            DirectorateCode.UEG
        ],
        MentionCategoryName.INSTITUTIONAL_BALANCES_AND_RESULTS: [
            DirectorateCode.COGER,
            DirectorateCode.DIFIN,
            DirectorateCode.DIRCO,
            DirectorateCode.URI,
            DirectorateCode.UGR
        ],
        MentionCategoryName.INSTITUTIONAL_REGULATORY: [
            DirectorateCode.UCI
        ],
        MentionCategoryName.INSTITUTIONAL_SPEECHES: [
            DirectorateCode.UGR
        ],
        MentionCategoryName.INTERNATIONAL_GENERAL: [
            DirectorateCode.UNI
        ],
        MentionCategoryName.LEGAL_GENERAL: [
            DirectorateCode.DIJUR
        ],
        MentionCategoryName.MARKETING_COMMUNICATION_CHANNELS: [
            DirectorateCode.CRM,
            DirectorateCode.DIMAC_GERAL
        ],
        MentionCategoryName.MARKETING_CCBB: [
            DirectorateCode.DIMAC_GERAL,
            DirectorateCode.CCBB
        ],
        MentionCategoryName.MARKETING_CAMPAIGN_CONTENT: [
            DirectorateCode.DIMAC_GERAL
        ],
        MentionCategoryName.MARKETING_INVESTMENT: [
            DirectorateCode.UCI
        ],
        MentionCategoryName.MARKETING_EVENTS_PROMOTIONS: [
            DirectorateCode.DIMAC_GERAL
        ],
        MentionCategoryName.SYSTEM_INSTABILITY_GENERAL: [
            DirectorateCode.DIMEP,
            DirectorateCode.DITEC
        ],
        MentionCategoryName.POLITICAL_AGENDAS_GENERAL: [
            DirectorateCode.RESTRITO
        ],
        MentionCategoryName.PEOPLE_PUBLIC_CONTESTS: [
            DirectorateCode.DIPES,
            DirectorateCode.DIREO
        ],
        MentionCategoryName.PEOPLE_UNIONS: [
            DirectorateCode.DIPES
        ],
        MentionCategoryName.PEOPLE_EMPLOYEES: [
            DirectorateCode.DIPES
        ],
        MentionCategoryName.PRODUCTS_SERVICES_INVESTMENTS: [
            DirectorateCode.UCI
        ],
        MentionCategoryName.PRODUCTS_SERVICES_LOANS_AND_FINANCING: [
            DirectorateCode.DIEMP
        ],
        MentionCategoryName.PRODUCTS_SERVICES_LOYALTY_PROGRAM: [
            DirectorateCode.DIMEP
        ],
        MentionCategoryName.PRODUCTS_SERVICES_PAYMENT_METHOD: [
            DirectorateCode.DIMEP
        ],
        MentionCategoryName.PRODUCTS_SERVICES_PAYROLL: [
            DirectorateCode.DIMEP,
            DirectorateCode.DIGOV
        ],
        MentionCategoryName.CUSTOMER_RELATIONS_AGENCIES: [
            DirectorateCode.DIREC,
            DirectorateCode.DIVAR
        ],
        MentionCategoryName.CUSTOMER_RELATIONS_DIGITAL: [
            DirectorateCode.UAC,
            DirectorateCode.DINED
        ],
        MentionCategoryName.CUSTOMER_RELATIONS_TELEPHONIC: [
            DirectorateCode.UAC
        ],
        MentionCategoryName.CUSTOMER_RELATIONS_GENERAL_OPERATIONAL: [
            DirectorateCode.DIOPE
        ],
        MentionCategoryName.CUSTOMER_RELATIONS_ACCESSIBILITY: [
            DirectorateCode.DISEC,
            DirectorateCode.UAC
        ],
        MentionCategoryName.SECURITY_EXTERNAL_SCAMS_AND_FRAUDS: [
            DirectorateCode.USD,
            DirectorateCode.USI
        ],
        MentionCategoryName.SECURITY_ROBBERIES_AND_PHYSICAL_SECURITY: [
            DirectorateCode.DIVAR,
            DirectorateCode.USI
        ],
        MentionCategoryName.SECURITY_CORRUPTION: [
            DirectorateCode.USI
        ],
        MentionCategoryName.SECURITY_DATA_LEAKS: [
            DirectorateCode.USD,
            DirectorateCode.USI
        ],
        MentionCategoryName.TERRITORIES_SUSTAINABILITY: [
            DirectorateCode.DIMAC_GERAL,
            DirectorateCode.ASG
        ],
        MentionCategoryName.TERRITORIES_TECHNOLOGY: [
            DirectorateCode.DIMAC_GERAL,
            DirectorateCode.DINED,
            DirectorateCode.DITEC
        ],
        MentionCategoryName.TERRITORIES_CULTURE_AND_SPORTS: [
            DirectorateCode.DIMAC_GERAL
        ],
        MentionCategoryName.CREDIT_LIMIT_RELEASE_AND_MANAGEMENT: [
            DirectorateCode.DIVAR,
            DirectorateCode.DICRE
        ],
        MentionCategoryName.CREDIT_DEFAULT: [
            DirectorateCode.UCR,
            DirectorateCode.DIVAR
        ],
        MentionCategoryName.CREDIT_DEBT_RENEGOTIATION: [
            DirectorateCode.UCR
        ],
    }
