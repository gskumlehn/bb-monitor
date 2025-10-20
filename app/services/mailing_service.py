from typing import Iterable, List
from app.repositories.mailing_repository import MailingRepository

class MailingService:
    def save(self, email: str, directorate_code: str) -> None:
        MailingRepository.save(email, directorate_code)

    def delete(self, email: str, directorate_code: str) -> int:
        return MailingRepository.delete(email, directorate_code)

    def get_emails_by_directorates(self, codes: Iterable[str]) -> List[str]:
        return MailingRepository.get_emails_by_directorates(codes)
