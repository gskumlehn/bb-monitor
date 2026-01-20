from app.enums.directorate_codes import DirectorateCode
from app.infra.database import db
from app.models.mailing import Mailing
from app.repositories.base_repository import BaseRepository
from sqlalchemy import select, delete
from typing import Iterable, List

class MailingRepository(BaseRepository[Mailing]):
    model = Mailing

    @staticmethod
    def exists(email: str, directorate_code: str) -> bool:
        return db.session.execute(
            select(Mailing).where(
                Mailing.email == email,
                Mailing.directorate_code == directorate_code
            )
        ).scalar_one_or_none() is not None

    @staticmethod
    def delete(email: str, directorate_code: DirectorateCode) -> int:
        res = db.session.execute(
            delete(Mailing).where(
                Mailing.email == email,
                Mailing.directorate_code == directorate_code.name
            )
        )
        db.session.commit()

        return int(res.rowcount or 0)

    @staticmethod
    def get_emails_by_directorates(codes: Iterable[DirectorateCode]) -> List[str]:
        code_names = sorted({code.name for code in codes})
        q = select(Mailing.email).where(
            Mailing.directorate_code.in_(code_names)
        ).distinct().order_by(Mailing.email)

        return db.session.scalars(q).all()

    @staticmethod
    def list_directorates_by_email(email: str) -> List[str]:
        q = select(Mailing.directorate_code).where(
            Mailing.email == email
        ).distinct().order_by(Mailing.directorate_code)

        return db.session.scalars(q).all()
