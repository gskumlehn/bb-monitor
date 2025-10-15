# app/repositories/mailing_repository.py
from typing import Iterable, List
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from .models import Mailing

class MailingRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, email: str, directorate_code: str) -> None:
        email = (email or "").strip()
        directorate_code = (directorate_code or "").strip()
        if not email or not directorate_code:
            return

        exists = self.db.execute(
            select(Mailing).where(
                Mailing.email == email,
                Mailing.directorate_code == directorate_code
            )
        ).scalar_one_or_none()
        if exists:
            return

        self.db.add(Mailing(email=email, directorate_code=directorate_code))

    def remove(self, email: str, directorate_code: str) -> int:
        res = self.db.execute(
            delete(Mailing).where(
                Mailing.email == (email or "").strip(),
                Mailing.directorate_code == (directorate_code or "").strip()
            )
        )
        # SQLAlchemy 2.x: rowcount pode ser None dependendo do driver; normalizamos
        return int(res.rowcount or 0)

    def list_all(self) -> List[dict]:
        rows = self.db.execute(
            select(Mailing).order_by(Mailing.directorate_code, Mailing.email)
        ).scalars().all()
        return [{"email": r.email, "directorate_code": r.directorate_code} for r in rows]

    def get_emails_by_directorates(self, codes: Iterable[str]) -> List[str]:
        norm = sorted({(c or "").strip() for c in (codes or []) if c and c.strip()})
        if not norm:
            return []
        q = select(Mailing.email).where(Mailing.directorate_code.in_(norm)).distinct().order_by(Mailing.email)
        return [r[0] for r in self.db.execute(q).all()]

    def replace_directorate_emails(self, directorate_code: str, emails: List[str]) -> None:
        directorate_code = (directorate_code or "").strip()
        self.db.execute(delete(Mailing).where(Mailing.directorate_code == directorate_code))

        uniq = sorted({(e or "").strip() for e in (emails or []) if e and e.strip()})
        for e in uniq:
            self.db.add(Mailing(email=e, directorate_code=directorate_code))
