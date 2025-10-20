from typing import Iterable, List
from sqlalchemy import select, delete
from app.models.mailing import Mailing
from app.infra.bq_sa import get_session

class MailingRepository:
    @staticmethod
    def save(email: str, directorate_code: str) -> None:
        email = (email or "").strip()
        directorate_code = (directorate_code or "").strip()
        if not email or not directorate_code:
            return

        with get_session() as session:
            exists = session.execute(
                select(Mailing).where(
                    Mailing.email == email,
                    Mailing.directorate_code == directorate_code
                )
            ).scalar_one_or_none()
            if exists:
                return

            session.add(Mailing(email=email, directorate_code=directorate_code))
            session.commit()

    @staticmethod
    def delete(email: str, directorate_code: str) -> int:
        with get_session() as session:
            res = session.execute(
                delete(Mailing).where(
                    Mailing.email == (email or "").strip(),
                    Mailing.directorate_code == (directorate_code or "").strip()
                )
            )
            session.commit()
            return int(res.rowcount or 0)

    @staticmethod
    def get_emails_by_directorates(codes: Iterable[str]) -> List[str]:
        norm = sorted({(c or "").strip() for c in (codes or []) if c and c.strip()})
        if not norm:
            return []
        with get_session() as session:
            q = select(Mailing.email).where(Mailing.directorate_code.in_(norm)).distinct().order_by(Mailing.email)
            return [r[0] for r in session.execute(q).all()]
