from app.models.mailing_history import MailingHistory
from app.infra.bq_sa import get_session

class MailingHistoryRepository:
    @staticmethod
    def save(history: MailingHistory) -> MailingHistory:
        with get_session() as session:
            session.add(history)
            session.commit()
            return history
