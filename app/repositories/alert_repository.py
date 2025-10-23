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
    def get_by_hash(hash_id: str) -> Alert | None:
        if not hash_id:
            return None
        with get_session() as session:
            return session.execute(
                select(Alert).where(Alert.id == hash_id)
            ).scalar_one_or_none()

    @staticmethod
    def get_by_url(url: str) -> Alert | None:
        if not url:
            return None
        with get_session() as session:
            return session.execute(
                select(Alert).where(Alert.url == url)
            ).scalar_one_or_none()
