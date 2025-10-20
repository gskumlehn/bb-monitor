from app.infra.google_sheets import GoogleSheets
from app.services.ingestion_constants import IngestionConstants

class IngestionService:

    def __init__(self):
        self.google_sheets = GoogleSheets()
        from app.services.last_consumed_row_service import LastConsumedRowService
        self.last_consumed_row_service = LastConsumedRowService()

    def fetch_table_data(self):
        try:
            last_consumed_row = self.last_consumed_row_service.get_value()
            start_row = last_consumed_row + 1
            return self.google_sheets.get_sheet_data_with_start_row(
                IngestionConstants.SPREADSHEET_ID, IngestionConstants.NAMED_RANGE, start_row
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar dados da tabela: {e}")
