from app.infra.google_sheets import GoogleSheets
from app.constants.ingestion_constants import IngestionConstants
from app.custom_utils.date_utils import DateUtils
from app.services.alert_service import AlertService
from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus
from app.enums.stakeholders import Stakeholders
from app.enums.critical_topic import CriticalTopic
from app.enums.press_source import PressSource
from app.enums.social_media_source import SocialMediaSource
from app.enums.social_media_engagement import SocialMediaEngagement
from app.enums.repercussion import Repercussion
import logging
import pandas as pd
from typing import List, Sequence, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.services.mention_service import MentionService

logger = logging.getLogger(__name__)

class IngestionService:

    def ingest(self, start_row: int, end_row: int = None):
        if end_row is None:
            end_row = start_row

        alert_dicts = self.fetchParsedData(start_row, end_row)
        alerts = self.saveOrUpdateAlerts(alert_dicts)

        # executor = ThreadPoolExecutor(max_workers=1)
        # executor.submit(asyncio.run, self._trigger_mentions_creation(alerts))

        return {"message": "Alerta(s) ingerido(s) com sucesso.", "alerts": [alert.id for alert in alerts]}

    async def _trigger_mentions_creation(self, alerts: List[Any]):
        mention_service = MentionService()
        tasks = [mention_service.save(alert) for alert in alerts]

    def fetchParsedData(self, start_row: int, end_row: int) -> List[dict]:
        table_data = self.fetchTableData(start_row, end_row)
        return [self.parseTableRowToAlertDict(row) for row in table_data]

    def fetchTableData(self, start_row: int, end_row: int):
        google_sheets = GoogleSheets()
        dynamic_range = f"'{IngestionConstants.SHEET_NAME}'!{IngestionConstants.START_COL}{start_row}:{IngestionConstants.END_COL}{end_row}"
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
        alert_data["profiles_or_portals"] = self.parseListField(table_row.get("@ do perfil ou Nome do Portal"))
        alert_data["urls"] = self.parseListField(table_row.get("Link"))
        alert_data["title"] = table_row.get("Título").strip()
        alert_data["alert_text"] = self.clean_alert_text(table_row.get("Alerta (Texto)"))
        alert_data["criticality_level"] = CriticalityLevel(table_row.get("Nível de Criticidade").strip())
        alert_data["critical_topic"] = CriticalTopic.values_csv_to_type_list(table_row.get("Tema Crítico").strip()) if table_row.get("Tema Crítico") else []
        alert_data["press_sources"] = PressSource.values_csv_to_type_list(table_row.get("Emissor Imprensa").strip()) if table_row.get("Emissor Imprensa") else []
        alert_data["social_media_sources"] = SocialMediaSource.values_csv_to_type_list(table_row.get("Emissor Redes Sociais").strip()) if table_row.get("Emissor Redes Sociais") else []
        alert_data["stakeholders"] = Stakeholders.values_csv_to_type_list(table_row.get("Stakeholders").strip()) if table_row.get("Stakeholders") else []
        alert_data["social_media_engagements"] = SocialMediaEngagement.values_csv_to_type_list(table_row.get("Engajamento de redes sociais").strip()) if table_row.get("Engajamento de redes sociais") else []
        alert_data["repercussions"] = Repercussion.values_csv_to_type_list(table_row.get("Repercussão").strip()) if table_row.get("Repercussão") else []
        alert_data["history"] = table_row.get("Historico").strip() if table_row.get("Historico") else None

        return alert_data

    def clean_alert_text(self, value) -> str:
        if value is None:
            return ""
        text = str(value).strip()
        if not text:
            return ""

        lines = text.splitlines()

        first_idx = None
        for idx, line in enumerate(lines):
            if line.strip():
                first_idx = idx
                break

        if first_idx is not None and any(keyword in lines[first_idx].strip() for keyword in ["[RISCO DE REPUTAÇÃO BB]", "[RISCO DE REPUTAÇÃO]"]):
            del lines[first_idx]

        while lines and not lines[0].strip():
            del lines[0]

        if not lines:
            return ""

        found_line_idx = None
        for idx, line in enumerate(lines):
            if line.strip() == "FutureBrand":
                found_line_idx = idx
                break

        if found_line_idx is not None:
            if found_line_idx == len(lines) - 2:
                lines = lines[:found_line_idx]
            else:
                lines = lines[:found_line_idx]
            return "\n".join([l.rstrip() for l in lines]).strip()

        joined = "\n".join(lines)
        pos = joined.find("FutureBrand")
        if pos != -1:
            joined = joined[:pos].rstrip()
            return joined

        return joined.strip() if 'joined' in locals() else "\n".join(lines).strip()

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

    def saveOrUpdateAlerts(self, alert_dicts: List[dict]) -> List[Any]:
        return [saved_alert for alert_dict in alert_dicts if (saved_alert := self.saveOrUpdateAlert(alert_dict))]

    def saveOrUpdateAlert(self, alert_dict: dict) -> Any:
        alert_service = AlertService()
        return alert_service.save_or_update(alert_dict)