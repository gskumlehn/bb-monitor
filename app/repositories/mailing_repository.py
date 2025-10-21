from typing import Iterable, List
from sqlalchemy import select, delete
from app.models.mailing import Mailing
from app.infra.bq_sa import get_session
from app.enums.directorate_codes import DirectorateCode

class MailingRepository:
    @staticmethod
    def save(mailing: Mailing) -> None:
        with get_session() as session:
            exists = session.execute(
                select(Mailing).where(
                    Mailing.email == mailing.email,
                    Mailing.directorate_code == mailing._directorate_code
                )
            ).scalar_one_or_none()
            if exists:
                return

            session.add(mailing)
            session.commit()

    @staticmethod
    def delete(email: str, directorate_code: DirectorateCode) -> int:
        with get_session() as session:
            res = session.execute(
                delete(Mailing).where(
                    Mailing.email == email,
                    Mailing.directorate_code == directorate_code.name
                )
            )
            session.commit()

            return int(res.rowcount or 0)

    @staticmethod
    def get_emails_by_directorates(codes: Iterable[DirectorateCode]) -> List[str]:
        code_names = sorted({code.name for code in codes})
        with get_session() as session:
            q = select(Mailing.email).where(
                Mailing.directorate_code.in_(code_names)
            ).distinct().order_by(Mailing.email)

            return session.scalars(q).all()
