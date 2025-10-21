from sqlalchemy import select
from app.models.alert import Alert
from app.infra.bq_sa import get_session

class AlertRepository:

    @staticmethod
    def save(alert: Alert) -> None:
        with get_session() as session:
            exists = session.execute(
                select(Alert).where(
                    Alert.url == alert.url,
                )
            ).scalar_one_or_none()
            if exists:
                return

            session.add(alert)
            session.commit()
