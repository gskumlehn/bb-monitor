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

    def __init__(self):
        self.google_sheets = GoogleSheets()

    def ingest(self):
        table_data = self._fetch_table_data()
        alert_dicts = [self._convert_table_row_to_alert_dict(row) for row in table_data]

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
        date_str = table_row.get("Data de entrega")
        time_str = table_row.get("Horário")
        delivery_dt = None
        try:
            if date_str and time_str:
                delivery_dt = DateUtils.from_date_and_time(date_str, time_str)
        except Exception:
            delivery_dt = None

        alert_data = {
            "mailing_status": MailingStatus(table_row.get("Enviado ao Cliente?").strip()),
            "delivery_datetime": delivery_dt,
            "alert_types": AlertType.values_csv_to_type_list(table_row.get("Tipo").strip()),
            "criticality_level": CriticalityLevel(table_row.get("Nível de Criticidade").strip()),
            "profiles_or_portals": self.parse_list_field(table_row.get("@ do perfil ou Nome do Portal")),
            "urls": self.parse_list_field(table_row.get("Link")),
            "title": table_row.get("Título").strip(),
            "alert_text": table_row.get("Alerta (Texto)").strip(),
            "involved_variables": InvolvedVariables.values_csv_to_type_list(table_row.get("Variáveis Envolvidas").strip()),
            "stakeholders": Stakeholders.values_csv_to_type_list(table_row.get("Stakeholders").strip()),
            "history": table_row.get("Historico").strip() if table_row.get("Historico") else None,
        }

        return alert_data

    @staticmethod
    def parse_list_field(value) -> list[str]:
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
