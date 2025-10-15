import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Iterable, List

from bcr_api.bwproject import BWProject
from bcr_api.bwresources import BWQueries

class BrandwatchClient:

    def __init__(self):
        username = os.getenv("BW_EMAIL")
        password = os.getenv("BW_PASSWORD")
        project  = os.getenv("BW_PROJECT")

        if not username or not password or not project:
            raise RuntimeError("Credenciais BW ausentes: BW_EMAIL, BW_PASSWORD, BW_PROJECT")

        self._proj = BWProject(project=project, username=username, password=password)
        self._queries = BWQueries(self._proj)

    def get_filtered_mentions(
        self,
        query_name: str,
        start_datetime: datetime,
        end_datetime: datetime,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Recupera menções filtradas usando BWQueries.get_mentions do bcr-api.
        """
        start_iso = start_datetime.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_iso = end_datetime.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        results = self._queries.get_mentions(
            name=query_name,
            startDate=start_iso,
            endDate=end_iso,
            limit=limit,
            **(filters or {})
        )
        return results or []

    def iter_mentions(self, query_name: str, start_utc: datetime, end_utc: datetime, pagesize: int = 5000) -> Iterable[Dict[str, Any]]:
        start_iso = start_utc.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_iso   = end_utc.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        for page in self._queries.iter_mentions(
            name=query_name,
            startDate=start_iso,
            endDate=end_iso,
            pagesize=pagesize,
            iter_by_page=True,
        ):
            if not page:
                continue

            for m in page:
                yield m

    @staticmethod
    def match_by_url(m: Dict[str, Any], link: str) -> bool:
        link = (link or "").strip()

        if not link:
            return False

        candidates: List[str] = []

        for k in ("url", "originalUrl"):
            if m.get(k):
                candidates.append(str(m.get(k)))

        for arr_key in ("expandedUrls", "displayUrls", "shortUrls", "mediaUrls"):
            arr = m.get(arr_key) or []
            for u in arr:
                if u:
                    candidates.append(str(u))

        candidates = [c.strip() for c in candidates if c]

        for c in candidates:
            if link == c or link in c:
                return True

        return False

    @staticmethod
    def extract_categories(m: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "categories": m.get("categories") or [],
            "categoryDetails": m.get("categoryDetails") or [],
            "categoryMetrics": m.get("categoryMetrics") or {},
        }

    def get_first_match_in_window(self, query_name: str, link: str, start_utc: datetime, end_utc: datetime) -> Optional[Dict[str, Any]]:
        for m in self.iter_mentions(query_name=query_name, start_utc=start_utc, end_utc=end_utc):
            if self.match_by_url(m, link):
                return m

        return None
