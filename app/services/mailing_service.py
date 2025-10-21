from typing import Iterable, List, Union, Tuple
from app.repositories.mailing_repository import MailingRepository
from app.enums.directorate_codes import DirectorateCode
from app.constants.mailing_constants import MailingConstants
from app.constants.error_messages import ErrorMessages
from app.utils.email_utils import EmailUtils

class MailingService:

    def save(self, email: str, directorate_code: Union[str, DirectorateCode]) -> None:
        email_norm, directorate_code = self.validate_save(email, directorate_code)
        MailingRepository.save(email_norm, directorate_code)

    def validate_save(self, email: str, directorate_code: Union[str, DirectorateCode]) -> Tuple[str, DirectorateCode]:
        email_norm = self.validate_email(email)
        directorate_code = DirectorateCode.from_name(directorate_code)

        return email_norm, directorate_code

    def validate_email(self, email: str) -> str:
        email_norm = EmailUtils.normalize_email(email)
        if not email_norm:
            raise ValueError(ErrorMessages.model["Mailing.email.empty"])
        if not EmailUtils.is_valid_email(email_norm):
            raise ValueError(ErrorMessages.model["Mailing.email.invalid"])
        if not EmailUtils.is_allowed_domain(email_norm, MailingConstants.ALLOWED_DOMAINS):
            raise ValueError(ErrorMessages.model["Mailing.email.domain.invalid"])
        return email_norm

    def delete(self, email: str, directorate_code: str) -> int:
        return MailingRepository.delete(EmailUtils.normalize_email(email), DirectorateCode.from_name(directorate_code))

    def get_emails_by_directorates(self, codes: Iterable[DirectorateCode]) -> List[str]:
        return MailingRepository.get_emails_by_directorates(codes)
