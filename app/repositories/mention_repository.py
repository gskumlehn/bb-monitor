from app.models.mention import Mention
from app.infra.bq_sa import get_session
from typing import List

class MentionRepository:

    @staticmethod
    def save(mention: Mention) -> Mention:
        with get_session() as session:
            session.add(mention)
            session.commit()
            return mention

    @staticmethod
    def find_by_alert_id(alert_id: str) -> List[Mention]:
        with get_session() as session:
            return session.query(Mention).filter(Mention.alert_id == alert_id).all()
