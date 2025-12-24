from app.infra.database import db
from app.models.alert import Alert
from app.repositories.base_repository import BaseRepository
from sqlalchemy import select, func, extract
from typing import List, Optional

class AlertRepository(BaseRepository[Alert]):
    model = Alert

    @staticmethod
    def get_max_sequential_id(code_year: int) -> Optional[int]:
        query = select(func.max(Alert.sequential_id)).where(Alert.code_year == code_year)
        max_id = db.session.execute(query).scalar_one_or_none()
        return max_id

    @staticmethod
    def get_max_sequential_version(sequential_id: int, code_year: int) -> Optional[int]:
        query = select(func.max(Alert.sequential_version)).where(
            Alert.sequential_id == sequential_id,
            Alert.code_year == code_year
        )
        max_version = db.session.execute(query).scalar_one_or_none()
        return max_version

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
