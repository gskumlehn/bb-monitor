from app.infra.google_sheets import GoogleSheets
from app.services.last_consumed_row_service import LastConsumedRowService

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
        self.last_consumed_row_service = LastConsumedRowService()

    def fetch_table_data(self):
        try:
            last_consumed_row = self.last_consumed_row_service.get_value()
            start_row = last_consumed_row + 1
            return self.google_sheets.get_sheet_data_with_start_row(
                self.SPREADSHEET_ID, self.NAMED_RANGE, start_row
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar dados da tabela: {e}")

