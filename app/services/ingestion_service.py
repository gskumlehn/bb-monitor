from app.infra.google_sheets import GoogleSheets

class IngestionService:
    SPREADSHEET_ID = "1yOD6bD_Syyv-zo5CtYXlCGMaWHIR12gUNzW1Zb7klbs"
    NAMED_RANGE = "Tabela1"
    EXPECTED_COLUMNS = [
        "Controle de Envio",
        "Data de entrega",
        "Horário",
        "Tipo",
        "Nível de Criticidade",
        "@ do perfil ou Nome do Portal",
        "Link",
        "Título",
        "Alerta (Texto)",
        "Variáveis Envolvidas",
        "Stakeholders",
        "Historico"
    ]

    def __init__(self):
        self.google_sheets = GoogleSheets()

    def fetch_table_data(self):
        try:
            return self.google_sheets.get_sheet_data(self.SPREADSHEET_ID, self.NAMED_RANGE)
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar dados da tabela: {e}")
