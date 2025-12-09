import re
from typing import Set
from markupsafe import Markup

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

    @staticmethod
    def linkify(text: str) -> Markup:
        if not text:
            return Markup("")

        s = text.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\\r', '\n')

        a_tags = {}
        def _protect_a(m):
            key = f"__A_TAG_{len(a_tags)}__"
            a_tags[key] = m.group(0)
            return key
        protected = re.sub(r'<a\b[^>]*?>.*?</a>', _protect_a, s, flags=re.IGNORECASE | re.DOTALL)

        url_pattern = re.compile(r'https?://[^\s<>()\[\]{}]+', flags=re.IGNORECASE)

        result_parts = []
        last_idx = 0
        for m in url_pattern.finditer(protected):
            start, end = m.start(), m.end()

            consume_start = start
            consume_end = end

            open_ch = ""
            if start - 1 >= 0 and protected[start - 1] in "([{":
                open_ch = protected[start - 1]
                consume_start = start - 1

            close_ch = ""
            if end < len(protected) and protected[end] in ")]}":
                close_ch = protected[end]
                consume_end = end + 1

            result_parts.append(protected[last_idx:consume_start])

            url = m.group(0)
            visible = f"{open_ch}{url}{close_ch}"
            anchor = f'<a href="{url}" style="display:inline; white-space:inherit; word-break:break-word;">{visible}</a>'
            result_parts.append(anchor)

            last_idx = consume_end

        result_parts.append(protected[last_idx:])
        linked = "".join(result_parts)

        for key, val in a_tags.items():
            linked = linked.replace(key, val)

        wrapped = f'<div style="white-space: pre-wrap;">{linked}</div>'
        return Markup(wrapped)

    @staticmethod
    def boldify(text: str) -> Markup:
        pattern = re.compile(r'(\*{1,2})(.+?)\1', flags=re.DOTALL)

        def replace_bold(match):
            content = match.group(2)
            return f"<b>{content}</b>"

        result = re.sub(pattern, replace_bold, text)
        return Markup(result)
