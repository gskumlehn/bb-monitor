from sqlalchemy import select
from app.models.mention import Mention
from app.infra.bq_sa import get_session

class MentionRepository:

    @staticmethod
    def save(mention: Mention) -> Mention:
        with get_session() as session:
            session.add(mention)
            session.commit()
            return mention

    @staticmethod
    def list_by_urls(urls: list[str]) -> list[Mention]:
        with get_session() as session:
            query = select(Mention).where(Mention.url.in_(urls))
            result = session.execute(query).scalars().all()
            return result
