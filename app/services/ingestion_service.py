from app.infra.google_sheets import GoogleSheets
from app.constants.ingestion_constants import IngestionConstants
from app.infra.brandwatch_client import BrandwatchClient
from app.utils.date_utils import DateUtils
from app.services.alert_service import AlertService

class IngestionService:

    def __init__(self):
        self.google_sheets = GoogleSheets()

    def ingest(self):
        table_data = self._fetch_table_data()
        alert_dicts = [self._convert_table_row_to_alert_dict(row) for row in table_data]
        alert_dicts = self._fetch_alert_guid(alert_dicts)

        alert_service = AlertService()
        alerts = [alert_service.save(alert_dict) for alert_dict in alert_dicts]

    def _fetch_table_data(self):
        dynamic_range = f"'{IngestionConstants.SHEET_NAME}'!{IngestionConstants.START_COL}:{IngestionConstants.END_COL}"
        return self.google_sheets.get_sheet_data_with_start_row(IngestionConstants.SPREADSHEET_ID, dynamic_range)

    def _convert_table_row_to_alert_dict(self, table_row: list) -> dict:
        alert_data = {
            "mailing_status": table_row[0],  # Controle de Envio
            "date": table_row[1],  # Data de entrega
            "time": table_row[2],  # Horário
            "alert_types": table_row[3],  # Tipo
            "criticality_level": table_row[4],  # Nível de Criticidade
            "profile_or_portal": table_row[5],  # @ do perfil ou Nome do Portal
            "url": table_row[6],  # Link
            "title": table_row[7],  # Título
            "alert_text": table_row[8],  # Alerta (Texto)
            "involved_variables": table_row[9],  # Variáveis Envolvidas
            "stakeholders": table_row[10],  # Stakeholders
            "history": table_row[11],  # Historico
        }

        return alert_data

    def _fetch_alert_guid(self, alert_dicts: list) -> list:
        bw_client = BrandwatchClient()

        for alert in alert_dicts:
            alert_datetime = DateUtils.from_date_and_time(alert.get("date"), alert.get("time"))
            alert["delivery_datetime"] = alert_datetime

            end_utc = alert_datetime
            start_utc = DateUtils.subtract_days(end_utc, days=7)

            mentions = bw_client.get_filtered_mentions(
                start_datetime=start_utc,
                end_datetime=end_utc,
                filters={"url": alert.get("url")},
                limit=1
            )

            if mentions and mentions[0].get("url") == alert.get("url"):
                alert["brandwatch_id"] = mentions[0].get("guid")

        return alert_dicts
