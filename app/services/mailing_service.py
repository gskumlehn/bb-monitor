from app.constants.error_messages import ErrorMessages
from app.constants.mailing_constants import MailingConstants
from app.custom_utils.email_utils import EmailUtils
from app.enums.directorate_codes import DirectorateCode
from app.models.mailing import Mailing
from app.repositories.mailing_repository import MailingRepository
from typing import Union, Tuple, List

class MailingService:

    def save(self, email: str, directorate_code: Union[str, DirectorateCode]) -> Mailing:
        email_norm, directorate_code = self.validate_save(email, directorate_code)

        mailing = Mailing()
        mailing.email = email_norm
        mailing.directorate_code = directorate_code

        MailingRepository.save(mailing)

        return mailing

    def validate_save(self, email: str, directorate_code: Union[str, DirectorateCode]) -> Tuple[str, DirectorateCode]:
        email_norm = self.validate_email(email)
        directorate_code = DirectorateCode.from_name(directorate_code)

        if MailingRepository.exists(email_norm, directorate_code.name):
            raise ValueError(ErrorMessages.model["Mailing.exists"])

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

    def list_by_directorate(self, directorate_code: str) -> List[str]:
        code = DirectorateCode.from_name(directorate_code)
        return MailingRepository.get_emails_by_directorates([code])

    def list_directorates_by_email(self, email: str) -> List[str]:
        email_norm = self.validate_email(email)
        return MailingRepository.list_directorates_by_email(email_norm)
