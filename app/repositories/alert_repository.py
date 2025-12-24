from sqlalchemy import select, extract
from app.models.alert import Alert
from app.repositories.base_repository import BaseRepository
from app.infra.database import db
from datetime import datetime
from typing import List, Optional

class AlertRepository(BaseRepository[Alert]):
    model = Alert

    @staticmethod
    def get_by_urls(urls: List[str]) -> Optional[Alert]:
        if not urls:
            return None
        
        sorted_urls = sorted(urls)
        query = select(Alert).where(Alert._urls == sorted_urls)
        return db.session.execute(query).scalars().first()

    @staticmethod
    def update(alert: Alert) -> Alert:
        merged = db.session.merge(alert)
        db.session.commit()
        return merged

    @staticmethod
    def list_by_month_year(month: int, year: int) -> List[Alert]:
        query = (
            select(Alert)
            .where(
                extract("month", Alert._delivery_datetime) == month,
                extract("year", Alert._delivery_datetime) == year
            )
            .order_by(Alert._delivery_datetime.asc())
        )
        return db.session.execute(query).scalars().all()

    @staticmethod
    def list_by_ids(alert_ids: List[str]) -> List[Alert]:
        query = (
            select(Alert)
            .where(Alert.id.in_(alert_ids))
            .order_by(Alert._delivery_datetime.asc())
        )
        return db.session.execute(query).scalars().all()
