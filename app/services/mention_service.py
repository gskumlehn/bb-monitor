import logging
from datetime import datetime
from typing import Optional, List, Dict

from app.custom_utils.date_utils import DateUtils
from app.infra.brandwatch_client import BrandwatchClient
from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)


class MentionService:
    def __init__(self):
        self._bw = BrandwatchClient()
        self.PAGE_SIZE = 100
        self.MAX_PAGES = 10

    def fetch_mention_by_url(
            self,
            url: str,
            end_datetime: datetime,
            days: int = 7,
            limit: int = 1
    ) -> Optional[Dict]:
        if not url or not end_datetime:
            logger.warning("URL ou end_datetime não fornecidos")
            return None

        try:
            mentions = self.fetch_mentions_with_params(
                filters={"url": url},
                end_datetime=end_datetime,
                days=days,
                limit=limit,
                page=1
            )

            if not mentions:
                mentions = self.fetch_mentions_with_params(
                    filters={"originalUrl": url},
                    end_datetime=end_datetime,
                    days=days,
                    limit=limit,
                    page=1
                )

            if mentions:
                if len(mentions) == 1:
                    return mentions[0]

            return None
        except Exception:
            logger.exception("Erro ao buscar mention no Brandwatch para url=%s", url)
            return None

    def _fetch_mention_by_url_paginated(
            self,
            url: str,
            url_id: str,
            end_datetime: datetime,
            days: int,
            page_size: int = 100
    ) -> Optional[Dict]:
        return None

    def fetch_mentions_with_params(
            self,
            filters: Dict[str, str],
            end_datetime: datetime,
            days: int = 7,
            limit: int = 100,
            page: Optional[int] = None
    ) -> List[Dict]:
        try:
            start_dt = DateUtils.subtract_days(end_datetime, days=days)
            if page is not None:
                try:
                    mentions = self._bw.get_filtered_mentions(
                        start_datetime=start_dt,
                        end_datetime=end_datetime,
                        filters=filters or {},
                        limit=limit,
                        page=page
                    )
                    return mentions or []
                except TypeError:
                    total_limit = limit * self.MAX_PAGES
                    mentions_all = self._bw.get_filtered_mentions(
                        start_datetime=start_dt,
                        end_datetime=end_datetime,
                        filters=filters or {},
                        limit=total_limit
                    ) or []
                    start_idx = (page - 1) * limit
                    end_idx = start_idx + limit
                    return mentions_all[start_idx:end_idx]
            else:
                mentions = self._bw.get_filtered_mentions(
                    start_datetime=start_dt,
                    end_datetime=end_datetime,
                    filters=filters or {},
                    limit=limit
                )
                return mentions or []
        except Exception:
            logger.exception(
                "Erro ao buscar mentions no Brandwatch com filtros=%s end=%s days=%s page=%s",
                filters, end_datetime, days, page
            )
            return []
