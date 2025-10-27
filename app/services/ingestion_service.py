from app.infra.google_sheets import GoogleSheets
from app.constants.ingestion_constants import IngestionConstants
from app.custom_utils.date_utils import DateUtils
from app.services.alert_service import AlertService
from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus
from app.enums.involved_variables import InvolvedVariables
from app.enums.stakeholders import Stakeholders
import logging
import pandas as pd
from typing import List, Sequence, Any

logger = logging.getLogger(__name__)

class IngestionService:

    def ingest(self):
        alert_dicts = self.fetchParsedData()
        alerts = self.saveAlerts(alert_dicts)

    def fetchParsedData(self) -> List[dict]:
        table_data = self.fetchTableData()
        return [self.parseTableRowToAlertDict(row) for row in table_data]

    def fetchTableData(self):
        google_sheets = GoogleSheets()
        dynamic_range = f"'{IngestionConstants.SHEET_NAME}'!{IngestionConstants.START_COL}33:{IngestionConstants.END_COL}"
        raw_data = google_sheets.get_sheet_data_with_start_row(IngestionConstants.SPREADSHEET_ID, dynamic_range)

        if not raw_data:
            return []

        normalized_rows = self.normalizeRows(raw_data, IngestionConstants.EXPECTED_COLUMNS)
        df = pd.DataFrame(data=normalized_rows, columns=IngestionConstants.EXPECTED_COLUMNS)

        return df.to_dict(orient="records")

    def normalizeRows(self, raw_rows: Sequence[Sequence[Any]], expected_cols: List[str]) -> List[List[Any]]:
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

    def parseTableRowToAlertDict(self, table_row: dict) -> dict:
        date_str = table_row.get("Data de entrega")
        time_str = table_row.get("Horário")
        delivery_dt = None

        try:
            if date_str and time_str:
                delivery_dt = DateUtils.from_date_and_time(date_str, time_str)
        except Exception:
            delivery_dt = None

        alert_data = {}
        alert_data["mailing_status"] = MailingStatus(table_row.get("Enviado ao Cliente?").strip())
        alert_data["delivery_datetime"] = delivery_dt
        alert_data["alert_types"] = AlertType.values_csv_to_type_list(table_row.get("Tipo").strip())
        alert_data["criticality_level"] = CriticalityLevel(table_row.get("Nível de Criticidade").strip())
        alert_data["profiles_or_portals"] = self.parseListField(table_row.get("@ do perfil ou Nome do Portal"))
        alert_data["urls"] = self.parseListField(table_row.get("Link"))
        alert_data["title"] = table_row.get("Título").strip()
        alert_data["alert_text"] = table_row.get("Alerta (Texto)").strip()
        alert_data["involved_variables"] = InvolvedVariables.values_csv_to_type_list(table_row.get("Variáveis Envolvidas").strip())
        alert_data["stakeholders"] = Stakeholders.values_csv_to_type_list(table_row.get("Stakeholders").strip())
        alert_data["history"] = table_row.get("Historico").strip() if table_row.get("Historico") else None

        return alert_data

    def parseListField(self, value) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [v.strip() for v in value if isinstance(v, str) and v.strip()]
        if isinstance(value, str):
            if "\r\n" in value or "\n" in value:
                parts = [p.strip() for p in value.splitlines() if p.strip()]
                if parts:
                    return parts
            return [p.strip() for p in value.split(",") if p.strip()]
        return []

    def saveAlerts(self, alert_dicts: List[dict]) -> List[Any]:
        return [saved_alert for alert_dict in alert_dicts if (saved_alert := self.saveAlert(alert_dict))]

    def saveAlert(self, alert_dict: dict) -> Any:
        alert_service = AlertService()
        try:
            return alert_service.save(alert_dict)
        except ValueError as e:
            logger.error(f"Erro de validação ao salvar alerta: {e}")
            return None
        except Exception:
            logger.exception("Erro inesperado ao salvar alerta durante ingest")
            return None
