from sqlalchemy import select, update
from app.models.last_consumed_row import LastConsumedRow
from app.infra.bq_sa import get_session

class LastConsumedRowRepository:

    @staticmethod
    def update_value(value: int) -> None:
        with get_session() as session:
            session.execute(
                update(LastConsumedRow).values(value=value)
            )
            session.commit()

    @staticmethod
    def load_value() -> int:
        with get_session() as session:
            last_consumed_row = session.execute(
                select(LastConsumedRow.value)
            ).scalar_one_or_none()
            return last_consumed_row if last_consumed_row is not None else 2
