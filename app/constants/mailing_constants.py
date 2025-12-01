from app.enums.mention_category_name import MentionCategoryName
from app.enums.directorate_codes import DirectorateCode

class MailingConstants:
    ALLOWED_DOMAINS = {
        "futurebrand.com",
        "futurebrand.com.br",
        "bb.com.br"
    }

    CATEGORY_TO_DIRECTORATE_MAP = {
        MentionCategoryName.HARASSMENT_OR_PAY_INEQUITY: [
            DirectorateCode.ASG,
            DirectorateCode.DIPES
        ],
        MentionCategoryName.HUMAN_RIGHTS_AND_DIVERSITY: [
            DirectorateCode.ASG
        ],
        MentionCategoryName.SUSTAINABILITY_IN_AGRO: [
            DirectorateCode.DIRAG,
            DirectorateCode.ASG
        ],
        MentionCategoryName.PROGRAMS_FOR_AGRO: [
            DirectorateCode.DIRAG,
            DirectorateCode.DIGOV
        ],
        MentionCategoryName.GENERAL_AGRO_OPERATIONS: [
            DirectorateCode.DIRAG
        ],
        MentionCategoryName.BB_ASSET: [
            DirectorateCode.BB_ASSET,
            DirectorateCode.UPE
        ],
        MentionCategoryName.BB_SECURITIES: [
            DirectorateCode.BB_SEGUROS,
            DirectorateCode.UPE
        ],
        MentionCategoryName.BB_CONSORTIUM: [
            DirectorateCode.UPE,
            DirectorateCode.BB_CONSORCIOS
        ],
        MentionCategoryName.GENERAL_COLLABORATES: [
            DirectorateCode.UPE
        ],
        MentionCategoryName.CORPORATE_POLICIES: [
            DirectorateCode.DIREO
        ],
        MentionCategoryName.AGENCY_GOALS_AND_BUSINESS: [
            DirectorateCode.DIVAR
        ],
        MentionCategoryName.FINANCE: [
            DirectorateCode.DIFIN,
            DirectorateCode.URI,
            DirectorateCode.UCI,
            DirectorateCode.TESOURARIA_GLOBAL,
            DirectorateCode.COGER
        ],
        MentionCategoryName.SUPPLIER: [
            DirectorateCode.DISEC
        ],
        MentionCategoryName.COMPLIANCE: [
            DirectorateCode.DICOI,
            DirectorateCode.DITEC
        ],
        MentionCategoryName.FEDERAL_RESOURCE_PROGRAM: [
            DirectorateCode.DIGOV,
            DirectorateCode.UEG
        ],
        MentionCategoryName.BALANCES_AND_RESULTS: [
            DirectorateCode.COGER,
            DirectorateCode.DIFIN,
            DirectorateCode.DIRCO,
            DirectorateCode.URI,
            DirectorateCode.UGR
        ],
        MentionCategoryName.REGULATORY: [
            DirectorateCode.UCI
        ],
        MentionCategoryName.INSTITUTIONAL_SPEECHES: [
            DirectorateCode.UGR
        ],
        MentionCategoryName.INTERNATIONAL: [
            DirectorateCode.UNI
        ],
        MentionCategoryName.LEGAL: [
            DirectorateCode.DIJUR
        ],
        MentionCategoryName.COMMUNICATION_CHANNELS_OR_SEGMENTATION: [
            DirectorateCode.CRM,
            DirectorateCode.DIMAC_GERAL
        ],
        MentionCategoryName.CCBB: [
            DirectorateCode.DIMAC_GERAL,
            DirectorateCode.CCBB
        ],
        MentionCategoryName.CAMPAIGN_CONTENT: [
            DirectorateCode.DIMAC_GERAL
        ],
        MentionCategoryName.INVESTMENT: [
            DirectorateCode.UCI
        ],
        MentionCategoryName.EVENTS_PROMOTIONS_OR_SPONSORSHIPS: [
            DirectorateCode.DIMAC_GERAL
        ],
        MentionCategoryName.SYSTEM_INSTABILITY: [
            DirectorateCode.DIMEP,
            DirectorateCode.DITEC
        ],
        MentionCategoryName.POLITICAL_AGENDAS: [
            DirectorateCode.RESTRITO
        ],
        MentionCategoryName.UNIONS_OR_PUBLIC_CONTESTS: [
            DirectorateCode.DIPES,
            DirectorateCode.DIREO
        ],
        MentionCategoryName.EMPLOYEES: [
            DirectorateCode.DIPES
        ],
        MentionCategoryName.INVESTMENTS: [
            DirectorateCode.UCI
        ],
        MentionCategoryName.LOANS_AND_FINANCING: [
            DirectorateCode.DIEMP
        ],
        MentionCategoryName.LOYALTY_PROGRAM: [
            DirectorateCode.DIMEP
        ],
        MentionCategoryName.PAYMENT_METHOD: [
            DirectorateCode.DIMEP
        ],
        MentionCategoryName.PAYROLL: [
            DirectorateCode.DIMEP,
            DirectorateCode.DIGOV
        ],
        MentionCategoryName.AGENCIES: [
            DirectorateCode.DIREC,
            DirectorateCode.DIVAR
        ],
        MentionCategoryName.DIGITAL: [
            DirectorateCode.UAC,
            DirectorateCode.DINED
        ],
        MentionCategoryName.TELEPHONIC: [
            DirectorateCode.UAC
        ],
        MentionCategoryName.GENERAL_OPERATIONAL: [
            DirectorateCode.DIOPE
        ],
        MentionCategoryName.ACCESSIBILITY: [
            DirectorateCode.DISEC,
            DirectorateCode.UAC
        ],
        MentionCategoryName.INTERNAL_SCAMS_AND_FRAUDS: [
            DirectorateCode.USI,
            DirectorateCode.DIPES
        ],
        MentionCategoryName.EXTERNAL_SCAMS_AND_FRAUDS: [
            DirectorateCode.USD,
            DirectorateCode.USI
        ],
        MentionCategoryName.ROBBERIES_AND_PHYSICAL_SECURITY: [
            DirectorateCode.DIVAR,
            DirectorateCode.USI
        ],
        MentionCategoryName.CORRUPTION: [
            DirectorateCode.USI
        ],
        MentionCategoryName.DATA_LEAKS: [
            DirectorateCode.USD,
            DirectorateCode.USI
        ],
        MentionCategoryName.SUSTAINABILITY: [
            DirectorateCode.DIMAC_GERAL,
            DirectorateCode.ASG
        ],
        MentionCategoryName.TECHNOLOGY: [
            DirectorateCode.DIMAC_GERAL,
            DirectorateCode.DINED,
            DirectorateCode.DITEC
        ],
        MentionCategoryName.CULTURE_AND_SPORTS: [
            DirectorateCode.DIMAC_GERAL
        ],
        MentionCategoryName.LIMIT_RELEASE_AND_MANAGEMENT: [
            DirectorateCode.DIVAR,
            DirectorateCode.DICRE
        ],
        MentionCategoryName.DEFAULT: [
            DirectorateCode.UCR,
            DirectorateCode.DIVAR
        ],
        MentionCategoryName.DEBT_RENEGOTIATION: [
            DirectorateCode.UCR
        ],
    }
