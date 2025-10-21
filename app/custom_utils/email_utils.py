import re
from typing import Set

class EmailUtils:
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    @staticmethod
    def normalize_email(email: str) -> str:
        if not email:
            return ""

        return email.strip().lower()

    @staticmethod
    def is_valid_email(email: str) -> bool:
        normalized = EmailUtils.normalize_email(email)
        if not normalized:
            return False

        return bool(EmailUtils.EMAIL_RE.match(normalized))

    @staticmethod
    def is_allowed_domain(email: str, allowed_domains: Set[str]) -> bool:
        normalized = EmailUtils.normalize_email(email)
        if not normalized:
            return False

        domain = normalized.split("@", 1)[1] if "@" in normalized else normalized

        return domain in allowed_domains
