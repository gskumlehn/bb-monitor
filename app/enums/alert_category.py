from app.interfaces.enum_interface import EnumInterface
from app.enums.alert_subcategory import AlertSubcategory

class AlertCategory(EnumInterface):

    ESG = "OPERAÇÃO BB :: ASG"
    AGRIBUSINESS = "OPERAÇÃO BB :: Agronegócio"
    RELATED_ENTITIES = "OPERAÇÃO BB :: Coligadas e entidades relacionadas"
    STRATEGY = "OPERAÇÃO BB :: Estratégia"
    FINANCE = "OPERAÇÃO BB :: Finanças"
    SUPPLIER = "OPERAÇÃO BB :: Fornecedor"
    GOVERNANCE = "OPERAÇÃO BB :: Governança"
    INSTITUTIONAL = "OPERAÇÃO BB :: Institucional"
    INTERNATIONAL = "OPERAÇÃO BB :: Internacional"
    LEGAL = "OPERAÇÃO BB :: Jurídico"
    MARKETING_COMMUNICATION = "OPERAÇÃO BB :: Marketing e Comunicação"
    SYSTEM_INSTABILITY = "OPERAÇÃO BB :: Instabilidade de sistema"
    POLITICAL_AGENDAS = "OPERAÇÃO BB :: Pautas políticas"
    PEOPLE = "OPERAÇÃO BB :: Pessoas"
    PRODUCTS_SERVICES = "OPERAÇÃO BB :: Produtos/ Serviços"
    CUSTOMER_RELATIONS = "OPERAÇÃO BB :: Relacionamento e atendimento"
    SECURITY = "OPERAÇÃO BB :: Segurança"
    TERRITORIES = "OPERAÇÃO BB :: Territórios"
    CREDIT = "OPERAÇÃO BB :: Crédito"

    @classmethod
    def parse_from_subcategories(cls, subcategories: list[AlertSubcategory]) -> list["AlertCategory"]:
        CATEGORY_MAP = {
            AlertSubcategory.ESG_HARASSMENT_OR_PAY_INEQUITY: AlertCategory.ESG,
            AlertSubcategory.ESG_HUMAN_RIGHTS_AND_DIVERSITY: AlertCategory.ESG,
            AlertSubcategory.AGRIBUSINESS_SUSTAINABILITY_IN_AGRO: AlertCategory.AGRIBUSINESS,
            AlertSubcategory.AGRIBUSINESS_PROGRAMS_FOR_AGRO: AlertCategory.AGRIBUSINESS,
            AlertSubcategory.AGRIBUSINESS_GENERAL_AGRO_OPERATIONS: AlertCategory.AGRIBUSINESS,
            AlertSubcategory.RELATED_ENTITIES_BB_ASSET: AlertCategory.RELATED_ENTITIES,
            AlertSubcategory.RELATED_ENTITIES_SECURITIES: AlertCategory.RELATED_ENTITIES,
            AlertSubcategory.RELATED_ENTITIES_BB_CONSORTIUM: AlertCategory.RELATED_ENTITIES,
            AlertSubcategory.RELATED_ENTITIES_GENERAL_COLLABORATES: AlertCategory.RELATED_ENTITIES,
            AlertSubcategory.STRATEGY_CORPORATE_POLICIES: AlertCategory.STRATEGY,
            AlertSubcategory.STRATEGY_AGENCY_GOALS_AND_BUSINESS: AlertCategory.STRATEGY,
            AlertSubcategory.FINANCE_ACCOUNTING_AND_TREASURY: AlertCategory.FINANCE,
            AlertSubcategory.SUPPLIER_GENERAL: AlertCategory.SUPPLIER,
            AlertSubcategory.GOVERNANCE_COMPLIANCE: AlertCategory.GOVERNANCE,
            AlertSubcategory.GOVERNANCE_FEDERAL_RESOURCE_PROGRAM: AlertCategory.GOVERNANCE,
            AlertSubcategory.INSTITUTIONAL_BALANCES_AND_RESULTS: AlertCategory.INSTITUTIONAL,
            AlertSubcategory.INSTITUTIONAL_REGULATORY: AlertCategory.INSTITUTIONAL,
            AlertSubcategory.INSTITUTIONAL_SPEECHES: AlertCategory.INSTITUTIONAL,
            AlertSubcategory.INTERNATIONAL_GENERAL: AlertCategory.INTERNATIONAL,
            AlertSubcategory.LEGAL_GENERAL: AlertCategory.LEGAL,
            AlertSubcategory.MARKETING_COMMUNICATION_CHANNELS: AlertCategory.MARKETING_COMMUNICATION,
            AlertSubcategory.MARKETING_CCBB: AlertCategory.MARKETING_COMMUNICATION,
            AlertSubcategory.MARKETING_CAMPAIGN_CONTENT: AlertCategory.MARKETING_COMMUNICATION,
            AlertSubcategory.MARKETING_INVESTMENT: AlertCategory.MARKETING_COMMUNICATION,
            AlertSubcategory.MARKETING_EVENTS_PROMOTIONS: AlertCategory.MARKETING_COMMUNICATION,
            AlertSubcategory.SYSTEM_INSTABILITY_GENERAL: AlertCategory.SYSTEM_INSTABILITY,
            AlertSubcategory.POLITICAL_AGENDAS_GENERAL: AlertCategory.POLITICAL_AGENDAS,
            AlertSubcategory.PEOPLE_PUBLIC_CONTESTS: AlertCategory.PEOPLE,
            AlertSubcategory.PEOPLE_UNIONS: AlertCategory.PEOPLE,
            AlertSubcategory.PEOPLE_EMPLOYEES: AlertCategory.PEOPLE,
            AlertSubcategory.PRODUCTS_SERVICES_INVESTMENTS: AlertCategory.PRODUCTS_SERVICES,
            AlertSubcategory.PRODUCTS_SERVICES_LOANS_AND_FINANCING: AlertCategory.PRODUCTS_SERVICES,
            AlertSubcategory.PRODUCTS_SERVICES_LOYALTY_PROGRAM: AlertCategory.PRODUCTS_SERVICES,
            AlertSubcategory.PRODUCTS_SERVICES_PAYMENT_METHOD: AlertCategory.PRODUCTS_SERVICES,
            AlertSubcategory.PRODUCTS_SERVICES_PAYROLL: AlertCategory.PRODUCTS_SERVICES,
            AlertSubcategory.CUSTOMER_RELATIONS_AGENCIES: AlertCategory.CUSTOMER_RELATIONS,
            AlertSubcategory.CUSTOMER_RELATIONS_DIGITAL: AlertCategory.CUSTOMER_RELATIONS,
            AlertSubcategory.CUSTOMER_RELATIONS_TELEPHONIC: AlertCategory.CUSTOMER_RELATIONS,
            AlertSubcategory.CUSTOMER_RELATIONS_GENERAL_OPERATIONAL: AlertCategory.CUSTOMER_RELATIONS,
            AlertSubcategory.CUSTOMER_RELATIONS_ACCESSIBILITY: AlertCategory.CUSTOMER_RELATIONS,
            AlertSubcategory.SECURITY_EXTERNAL_SCAMS_AND_FRAUDS: AlertCategory.SECURITY,
            AlertSubcategory.SECURITY_ROBBERIES_AND_PHYSICAL_SECURITY: AlertCategory.SECURITY,
            AlertSubcategory.SECURITY_CORRUPTION: AlertCategory.SECURITY,
            AlertSubcategory.SECURITY_DATA_LEAKS: AlertCategory.SECURITY,
            AlertSubcategory.TERRITORIES_SUSTAINABILITY: AlertCategory.TERRITORIES,
            AlertSubcategory.TERRITORIES_TECHNOLOGY: AlertCategory.TERRITORIES,
            AlertSubcategory.TERRITORIES_CULTURE_AND_SPORTS: AlertCategory.TERRITORIES,
            AlertSubcategory.CREDIT_LIMIT_RELEASE_AND_MANAGEMENT: AlertCategory.CREDIT,
            AlertSubcategory.CREDIT_DEFAULT: AlertCategory.CREDIT,
            AlertSubcategory.CREDIT_DEBT_RENEGOTIATION: AlertCategory.CREDIT,
        }

        return list({CATEGORY_MAP[subcategory] for subcategory in subcategories})
