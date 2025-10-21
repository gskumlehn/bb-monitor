from app.infra.google_sheets import GoogleSheets
from app.constants.ingestion_constants import IngestionConstants

class IngestionService:

    def __init__(self):
        self.google_sheets = GoogleSheets()

    def fetch_table_data(self):
        try:
            dynamic_range = f"'{IngestionConstants.SHEET_NAME}'!{IngestionConstants.START_COL}:{IngestionConstants.END_COL}"
            return self.google_sheets.get_sheet_data_with_start_row(
                IngestionConstants.SPREADSHEET_ID, dynamic_range
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar dados da tabela: {e}")
