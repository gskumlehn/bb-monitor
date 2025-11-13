from app.models.mailing_history import MailingHistory
from app.infra.bq_sa import get_session
from sqlalchemy.orm.exc import NoResultFound

class MailingHistoryRepository:
    @staticmethod
    def save(history: MailingHistory) -> MailingHistory:
        with get_session() as session:
            session.add(history)
            session.commit()
            return history

    @staticmethod
    def delete_by_id(history_id: str):
        with get_session() as session:
            try:
                history = session.query(MailingHistory).filter_by(id=history_id).one()
                session.delete(history)
                session.commit()
            except NoResultFound:
                pass  # Handle case where the record does not exist
