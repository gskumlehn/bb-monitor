from app.models.mention import Mention
from app.infra.bq_sa import get_session

class MentionRepository:

    @staticmethod
    def save(mention: Mention) -> Mention:
        with get_session() as session:
            session.add(mention)
            session.commit()
            return mention