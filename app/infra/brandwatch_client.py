from datetime import datetime
from typing import Dict, Any, Optional, Iterable, List
import os

from bcr_api.bwproject import BWProject
from bcr_api.bwresources import BWQueries
from app.custom_utils.date_utils import DateUtils

class BrandwatchClient:

    def __init__(self):
        project = BWProject(
            project=os.getenv("BW_PROJECT"),
            username=os.getenv("BW_EMAIL"),
            password=os.getenv("BW_PASSWORD")
        )

        self.queries = BWQueries(project)
        self.queryName = os.getenv("BW_QUERY_NAME")

    def get_filtered_mentions(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        start_iso = DateUtils.to_iso_format(start_datetime)
        end_iso = DateUtils.to_iso_format(end_datetime)

        results = self.queries.get_mentions(
            name=self.queryName,
            startDate=start_iso,
            endDate=end_iso,
            limit=limit,
            **(filters or {})
        )
        return results or []

    @staticmethod
    def extract_categories(m: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "categories": m.get("categories") or [],
            "categoryDetails": m.get("categoryDetails") or [],
            "categoryMetrics": m.get("categoryMetrics") or {},
        }

