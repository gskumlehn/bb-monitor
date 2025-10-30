from sqlalchemy import select, func
from app.models.alert import Alert
from app.infra.bq_sa import get_session

class AlertRepository:

    @staticmethod
    def save(alert: Alert) -> Alert:
        alert.normalize_urls()
        with get_session() as session:
            session.add(alert)
            session.commit()
            return alert

    @staticmethod
    def get_by_urls(urls: list[str]) -> Alert | None:
        if not urls:
            return None

        sorted_urls_str = ",".join(sorted(urls))
        with get_session() as session:
            query = (
                select(Alert)
                .where(
                    func.array_to_string(Alert._urls, ",") == sorted_urls_str
                )
            )
            return session.execute(query).scalars().first()


    @staticmethod
    def delete_by_id(alert_id: str) -> None:
        with get_session() as session:
            session.query(Alert).filter_by(id=alert_id).delete()
            session.commit()

    @staticmethod
    def get_by_id(alert_id: str) -> Alert | None:
        with get_session() as session:
            return session.query(Alert).filter_by(id=alert_id).first()

    @staticmethod
    def update(alert: Alert) -> Alert | None:
        with get_session() as session:
            merged = session.merge(alert)
            session.commit()
            session.refresh(merged)
            return merged

    @staticmethod
    def list_by_month_year(month: int, year: int) -> list[Alert]:
        with get_session() as session:
            query = (
                select(Alert)
                .where(
                    func.extract("month", Alert._delivery_datetime) == month,
                    func.extract("year", Alert._delivery_datetime) == year
                )
                .order_by(Alert._delivery_datetime.asc())
            )
            return session.execute(query).scalars().all()
