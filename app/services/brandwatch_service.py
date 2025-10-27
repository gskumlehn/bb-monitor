from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from app.infra.brandwatch_client import BrandwatchClient
from app.custom_utils.date_utils import DateUtils

class BrandwatchService:

    def __init__(self):
        self._client = BrandwatchClient()

    def get_filtered_mentions(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        start_iso = DateUtils.to_iso_format(start_datetime)
        end_iso = DateUtils.to_iso_format(end_datetime)

        results = self._client.queries.get_mentions(
            name=self._client.queryName,
            startDate=start_iso,
            endDate=end_iso,
            limit=limit,
            **(filters or {})
        )
        return results or []

    def fetch_mention_by_url(
        self,
        url: str,
        start_date: datetime,
        end_date: datetime
    ) -> Optional[Dict]:
        try:
            filters = {
                'startDate': DateUtils.to_iso_format(start_date),
                'endDate': DateUtils.to_iso_format(end_date)
            }

            for mention in self._client.queries.iter_mentions(name=self._client.queryName, **filters):
                if self._is_match(mention, url):
                    return mention

            return None

        except Exception:
            return None

    def fetch_mention_by_url_with_retry(
        self,
        url: str,
        end_date: datetime,
        max_days_back: int = 30,
        interval: int = 2
    ) -> Optional[Dict]:
        for start_offset in range(0, max_days_back, interval):
            start_date = end_date - timedelta(days=start_offset + interval)
            current_end_date = end_date - timedelta(days=start_offset)

            mention = self.fetch_mention_by_url(
                url=url,
                start_date=start_date,
                end_date=current_end_date
            )
            if mention:
                return mention

        return None

    def _is_match(self, mention: Dict, original_url: str) -> bool:
        mention_url = mention.get('url', '')
        mention_original_url = mention.get('originalUrl', '')
        mention_thread_url = mention.get('threadURL', '')

        if original_url in {mention_url, mention_original_url, mention_thread_url}:
            return True

        mention_url_clean = mention_url.split('?')[0].split('#')[0].rstrip('/') if mention_url else ''
        original_url_clean = original_url.split('?')[0].split('#')[0].rstrip('/') if original_url else ''

        return mention_url_clean == original_url_clean
