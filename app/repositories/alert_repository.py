from sqlalchemy import select
from app.models.alert import Alert
from app.infra.bq_sa import get_session

class AlertRepository:

    @staticmethod
    def save(alert: Alert) -> Alert:
        with get_session() as session:
            session.add(alert)
            session.commit()
            return alert

    @staticmethod
    def get_by_urls(urls: list[str]) -> Alert | None:
        with get_session() as session:
            query = select(Alert).where(Alert._urls.overlap(urls))
            result = session.execute(query).scalars().first()
            return result
