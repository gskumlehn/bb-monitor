from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging
from app.infra.brandwatch_client import BrandwatchClient
from app.custom_utils.date_utils import DateUtils

class BrandwatchService:

    def __init__(self):
        self._client = BrandwatchClient()

    def fetch_mentions_by_urls_with_retry(
        self,
        urls: List[str],
        end_date: datetime,
        max_days_back: int = 30,
        interval: int = 2
    ) -> List[Dict[str, Any]]:
        matched_mentions = []
        remaining_urls = set(urls)

        for start_offset in range(0, max_days_back, interval):
            start_date = end_date - timedelta(days=start_offset + interval)
            current_end_date = end_date - timedelta(days=start_offset)

            try:
                filters = {
                    'startDate': DateUtils.to_iso_format(start_date),
                    'endDate': DateUtils.to_iso_format(current_end_date)
                }

                for mention in self._client.queries.iter_mentions(name=self._client.queryName, **filters):
                    for url in list(remaining_urls):
                        if self._is_match(mention, url):
                            matched_mentions.append({
                                "brandwatch_id": mention.get("guid"),
                                "url": url
                            })

                            remaining_urls.remove(url)
                            break

                if not remaining_urls:
                    break

            except Exception as e:
                logging.error(f"Erro ao buscar menções no intervalo {start_date} - {current_end_date}: {e}")
                continue

        if remaining_urls:
            logging.warning(f"As seguintes URLs não foram encontradas: {remaining_urls}")

        return matched_mentions

    def _is_match(self, mention: Dict, original_url: str) -> bool:
        mention_url = mention.get('url', '')
        mention_original_url = mention.get('originalUrl', '')
        mention_thread_url = mention.get('threadURL', '')

        if original_url in {mention_url, mention_original_url, mention_thread_url}:
            return True

        mention_url_clean = mention_url.split('?')[0].split('#')[0].rstrip('/') if mention_url else ''
        original_url_clean = original_url.split('?')[0].split('#')[0].rstrip('/') if original_url else ''

        return mention_url_clean == original_url_clean
