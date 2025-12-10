from app.interfaces.enum_interface import EnumInterface
from app.enums.alert_subcategory import AlertSubcategory
from app.constants.category_constants import CATEGORY_MAP

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
        return list({CATEGORY_MAP[subcategory] for subcategory in subcategories})
