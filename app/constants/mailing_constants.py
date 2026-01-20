from app.enums.alert_subcategory import AlertSubcategory
from app.enums.directorate_codes import DirectorateCode

class MailingConstants:
    ALLOWED_DOMAINS = {
        "futurebrand.com",
        "futurebrand.com.br",
        "bb.com.br"
    }

    SUBCATEGORY_TO_DIRECTORATE_MAP = {
        AlertSubcategory.ESG_HARASSMENT_OR_PAY_INEQUITY: [
            DirectorateCode.ASG,
            DirectorateCode.DIPES
        ],
        AlertSubcategory.ESG_HUMAN_RIGHTS_AND_DIVERSITY: [
            DirectorateCode.ASG
        ],
        AlertSubcategory.AGRIBUSINESS_SUSTAINABILITY_IN_AGRO: [
            DirectorateCode.DIRAG,
            DirectorateCode.ASG
        ],
        AlertSubcategory.AGRIBUSINESS_PROGRAMS_FOR_AGRO: [
            DirectorateCode.DIRAG,
            DirectorateCode.DIGOV
        ],
        AlertSubcategory.AGRIBUSINESS_GENERAL_AGRO_OPERATIONS: [
            DirectorateCode.DIRAG
        ],
        AlertSubcategory.RELATED_ENTITIES_BB_ASSET: [
            DirectorateCode.BB_ASSET,
            DirectorateCode.UPE
        ],
        AlertSubcategory.RELATED_ENTITIES_SECURITIES: [
            DirectorateCode.BB_SEGUROS,
            DirectorateCode.UPE
        ],
        AlertSubcategory.RELATED_ENTITIES_BB_CONSORTIUM: [
            DirectorateCode.UPE,
            DirectorateCode.BB_CONSORCIOS
        ],
        AlertSubcategory.RELATED_ENTITIES_GENERAL_COLLABORATES: [
            DirectorateCode.UPE
        ],
        AlertSubcategory.STRATEGY_CORPORATE_POLICIES: [
            DirectorateCode.DIREO
        ],
        AlertSubcategory.STRATEGY_AGENCY_GOALS_AND_BUSINESS: [
            DirectorateCode.DIVAR
        ],
        AlertSubcategory.FINANCE_ACCOUNTING_AND_TREASURY: [
            DirectorateCode.DIFIN,
            DirectorateCode.URI,
            DirectorateCode.UCI,
            DirectorateCode.TESOURARIA_GLOBAL,
            DirectorateCode.COGER
        ],
        AlertSubcategory.SUPPLIER_GENERAL: [
            DirectorateCode.DISEC
        ],
        AlertSubcategory.GOVERNANCE_COMPLIANCE: [
            DirectorateCode.DICOI,
            DirectorateCode.DITEC
        ],
        AlertSubcategory.GOVERNANCE_FEDERAL_RESOURCE_PROGRAM: [
            DirectorateCode.DIGOV,
            DirectorateCode.UEG
        ],
        AlertSubcategory.INSTITUTIONAL_BALANCES_AND_RESULTS: [
            DirectorateCode.COGER,
            DirectorateCode.DIFIN,
            DirectorateCode.DIRCO,
            DirectorateCode.URI,
            DirectorateCode.UGR
        ],
        AlertSubcategory.INSTITUTIONAL_REGULATORY: [
            DirectorateCode.UCI
        ],
        AlertSubcategory.INSTITUTIONAL_SPEECHES: [
            DirectorateCode.UGR
        ],
        AlertSubcategory.INTERNATIONAL_GENERAL: [
            DirectorateCode.UNI
        ],
        AlertSubcategory.LEGAL_GENERAL: [
            DirectorateCode.DIJUR
        ],
        AlertSubcategory.MARKETING_COMMUNICATION_CHANNELS: [
            DirectorateCode.CRM,
            DirectorateCode.DIMAC_GERAL
        ],
        AlertSubcategory.MARKETING_CCBB: [
            DirectorateCode.DIMAC_GERAL,
            DirectorateCode.CCBB
        ],
        AlertSubcategory.MARKETING_CAMPAIGN_CONTENT: [
            DirectorateCode.DIMAC_GERAL
        ],
        AlertSubcategory.MARKETING_INVESTMENT: [
            DirectorateCode.UCI
        ],
        AlertSubcategory.MARKETING_EVENTS_PROMOTIONS: [
            DirectorateCode.DIMAC_GERAL
        ],
        AlertSubcategory.SYSTEM_INSTABILITY_GENERAL: [
            DirectorateCode.DIMEP,
            DirectorateCode.DITEC
        ],
        AlertSubcategory.POLITICAL_AGENDAS_GENERAL: [
            DirectorateCode.RESTRITO
        ],
        AlertSubcategory.PEOPLE_PUBLIC_CONTESTS: [
            DirectorateCode.DIPES,
            DirectorateCode.DIREO
        ],
        AlertSubcategory.PEOPLE_UNIONS: [
            DirectorateCode.DIPES
        ],
        AlertSubcategory.PEOPLE_EMPLOYEES: [
            DirectorateCode.DIPES
        ],
        AlertSubcategory.PRODUCTS_SERVICES_INVESTMENTS: [
            DirectorateCode.UCI
        ],
        AlertSubcategory.PRODUCTS_SERVICES_LOANS_AND_FINANCING: [
            DirectorateCode.DIEMP
        ],
        AlertSubcategory.PRODUCTS_SERVICES_LOYALTY_PROGRAM: [
            DirectorateCode.DIMEP
        ],
        AlertSubcategory.PRODUCTS_SERVICES_PAYMENT_METHOD: [
            DirectorateCode.DIMEP
        ],
        AlertSubcategory.PRODUCTS_SERVICES_PAYROLL: [
            DirectorateCode.DIMEP,
            DirectorateCode.DIGOV
        ],
        AlertSubcategory.CUSTOMER_RELATIONS_AGENCIES: [
            DirectorateCode.CRM,
            DirectorateCode.DIREC,
            DirectorateCode.DIVAR
        ],
        AlertSubcategory.CUSTOMER_RELATIONS_DIGITAL: [
            DirectorateCode.UAC,
            DirectorateCode.DINED
        ],
        AlertSubcategory.CUSTOMER_RELATIONS_TELEPHONIC: [
            DirectorateCode.UAC
        ],
        AlertSubcategory.CUSTOMER_RELATIONS_GENERAL_OPERATIONAL: [
            DirectorateCode.DIOPE
        ],
        AlertSubcategory.CUSTOMER_RELATIONS_ACCESSIBILITY: [
            DirectorateCode.DISEC,
            DirectorateCode.UAC
        ],
        AlertSubcategory.SECURITY_EXTERNAL_SCAMS_AND_FRAUDS: [
            DirectorateCode.USD,
            DirectorateCode.USI
        ],
        AlertSubcategory.SECURITY_INTERNAL_SCAMS_AND_FRAUDS: [
            DirectorateCode.DIPES,
            DirectorateCode.USI
        ],
        AlertSubcategory.SECURITY_ROBBERIES_AND_PHYSICAL_SECURITY: [
            DirectorateCode.DIVAR,
            DirectorateCode.USI
        ],
        AlertSubcategory.SECURITY_CORRUPTION: [
            DirectorateCode.USI
        ],
        AlertSubcategory.SECURITY_DATA_LEAKS: [
            DirectorateCode.USD,
            DirectorateCode.USI
        ],
        AlertSubcategory.TERRITORIES_SUSTAINABILITY: [
            DirectorateCode.DIMAC_GERAL,
            DirectorateCode.ASG
        ],
        AlertSubcategory.TERRITORIES_TECHNOLOGY: [
            DirectorateCode.DIMAC_GERAL,
            DirectorateCode.DINED,
            DirectorateCode.DITEC
        ],
        AlertSubcategory.TERRITORIES_CULTURE_AND_SPORTS: [
            DirectorateCode.DIMAC_GERAL
        ],
        AlertSubcategory.CREDIT_LIMIT_RELEASE_AND_MANAGEMENT: [
            DirectorateCode.DIVAR,
            DirectorateCode.DICRE
        ],
        AlertSubcategory.CREDIT_DEFAULT: [
            DirectorateCode.UCR,
            DirectorateCode.DIVAR
        ],
        AlertSubcategory.CREDIT_DEBT_RENEGOTIATION: [
            DirectorateCode.UCR
        ],
    }
