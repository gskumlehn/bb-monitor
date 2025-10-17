from typing import Iterable, List
from sqlalchemy import select, delete
from app.models.mailing import Mailing
from app.infra.db import get_session

class MailingRepository:
    def __init__(self):
        self.session = get_session()

    def save(self, email: str, directorate_code: str) -> None:
        email = (email or "").strip()
        directorate_code = (directorate_code or "").strip()
        if not email or not directorate_code:
            return

        exists = self.session.execute(
            select(Mailing).where(
                Mailing.email == email,
                Mailing.directorate_code == directorate_code
            )
        ).scalar_one_or_none()
        if exists:
            return

        self.session.add(Mailing(email=email, directorate_code=directorate_code))
        self.session.commit()

    def delete(self, email: str, directorate_code: str) -> int:
        res = self.session.execute(
            delete(Mailing).where(
                Mailing.email == (email or "").strip(),
                Mailing.directorate_code == (directorate_code or "").strip()
            )
        )
        self.session.commit()
        return int(res.rowcount or 0)

    def get_emails_by_directorates(self, codes: Iterable[str]) -> List[str]:
        norm = sorted({(c or "").strip() for c in (codes or []) if c and c.strip()})
        if not norm:
            return []
        q = select(Mailing.email).where(Mailing.directorate_code.in_(norm)).distinct().order_by(Mailing.email)
        return [r[0] for r in self.session.execute(q).all()]
