from typing import Iterable, List
from app.repositories.mailing_repository import MailingRepository

class MailingService:
    def save(self, email: str, directorate_code: str) -> None:
        repository = MailingRepository()
        repository.save(email, directorate_code)

    def delete(self, email: str, directorate_code: str) -> int:
        repository = MailingRepository()
        return repository.delete(email, directorate_code)

    def get_emails_by_directorates(self, codes: Iterable[str]) -> List[str]:
        repository = MailingRepository()
        return repository.get_emails_by_directorates(codes)
