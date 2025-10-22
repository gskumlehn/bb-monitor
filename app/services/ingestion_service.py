from app.infra.google_sheets import GoogleSheets
from app.constants.ingestion_constants import IngestionConstants
from app.infra.brandwatch_client import BrandwatchClient
from app.custom_utils.date_utils import DateUtils
from app.services.alert_service import AlertService
import logging
import pandas as pd
from typing import List, Sequence, Any

logger = logging.getLogger(__name__)

class IngestionService:

    def __init__(self):
        self.google_sheets = GoogleSheets()

    def ingest(self):
        table_data = self._fetch_table_data()
        alert_dicts = [self._convert_table_row_to_alert_dict(row) for row in table_data]
        alert_dicts = self._fetch_alert_guid(alert_dicts)

        alert_service = AlertService()
        alerts = []
        for alert_dict in alert_dicts:
            try:
                saved = alert_service.save(alert_dict)
            except Exception:
                logger.exception("Erro ao salvar alert durante ingest")
                saved = None
            if saved:
                alerts.append(saved)

        return alerts

    def _normalize_rows(self, raw_rows: Sequence[Sequence[Any]], expected_cols: List[str]) -> List[List[Any]]:
        expected_len = len(expected_cols)
        normalized: List[List[Any]] = []
        for i, row in enumerate(raw_rows):
            row_list = list(row)
            if len(row_list) < expected_len:
                row_list.extend([None] * (expected_len - len(row_list)))
            elif len(row_list) > expected_len:
                main = row_list[: expected_len - 1]
                tail = row_list[expected_len - 1 :]
                tail_joined = " ".join([str(x) for x in tail if x is not None and str(x).strip() != ""])
                main.append(tail_joined if tail_joined != "" else None)
                row_list = main
            normalized.append(row_list)
        return normalized

    def _fetch_table_data(self):
        dynamic_range = f"'{IngestionConstants.SHEET_NAME}'!{IngestionConstants.START_COL}2:{IngestionConstants.END_COL}"
        raw_data = self.google_sheets.get_sheet_data_with_start_row(IngestionConstants.SPREADSHEET_ID, dynamic_range)

        if raw_data:
            normalized_rows = self._normalize_rows(raw_data, IngestionConstants.EXPECTED_COLUMNS)
            df = pd.DataFrame(data=normalized_rows, columns=IngestionConstants.EXPECTED_COLUMNS)
            return df.to_dict(orient="records")
        return []

    def _convert_table_row_to_alert_dict(self, table_row: dict) -> dict:
        alert_data = {
            "mailing_status": table_row.get("Controle de Envio"),
            "date": table_row.get("Data de entrega"),
            "time": table_row.get("Horário"),
            "alert_types": table_row.get("Tipo"),
            "criticality_level": table_row.get("Nível de Criticidade"),
            "profile_or_portal": table_row.get("@ do perfil ou Nome do Portal"),
            "url": table_row.get("Link"),
            "title": table_row.get("Título"),
            "alert_text": table_row.get("Alerta (Texto)"),
            "involved_variables": table_row.get("Variáveis Envolvidas"),
            "stakeholders": table_row.get("Stakeholders"),
            "history": table_row.get("Historico"),
        }

        return alert_data

    def _fetch_alert_guid(self, alert_dicts: list) -> list:
        bw_client = BrandwatchClient()

        for alert in alert_dicts:
            alert_datetime = DateUtils.from_date_and_time(alert.get("date"), alert.get("time"))
            alert["delivery_datetime"] = alert_datetime

            end_utc = alert_datetime
            start_utc = DateUtils.subtract_days(end_utc, days=10)

            mentions = bw_client.get_filtered_mentions(
                start_datetime=start_utc,
                end_datetime=end_utc,
                filters={"url": alert.get("url")},
                limit=1
            )

            if mentions and mentions[0].get("url") == alert.get("url"):
                alert["brandwatch_id"] = mentions[0].get("guid")

        return alert_dicts
