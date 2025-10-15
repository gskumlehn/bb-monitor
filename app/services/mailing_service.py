# app/services/mailing_service.py
from typing import Iterable, List
from app.infra.bq_sa import get_session
from app.repositories.mailing_repository import MailingRepository

class MailingService:
    def add(self, email: str, directorate_code: str) -> None:
        with get_session() as db:
            repo = MailingRepository(db)
            repo.add(email, directorate_code)

    def remove(self, email: str, directorate_code: str) -> int:
        with get_session() as db:
            repo = MailingRepository(db)
            return repo.remove(email, directorate_code)

    def list_all(self) -> List[dict]:
        with get_session() as db:
            repo = MailingRepository(db)
            return repo.list_all()

    def get_emails_by_directorates(self, codes: Iterable[str]) -> List[str]:
        with get_session() as db:
            repo = MailingRepository(db)
            return repo.get_emails_by_directorates(codes)

    def replace_directorate_emails(self, directorate_code: str, emails: List[str]) -> None:
        with get_session() as db:
            repo = MailingRepository(db)
            repo.replace_directorate_emails(directorate_code, emails)
