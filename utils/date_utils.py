from datetime import datetime
from zoneinfo import ZoneInfo

class DateUtils:
    BRAZIL_TZ = "America/Sao_Paulo"

    @staticmethod
    def to_iso_format(dt: datetime, tz: str = BRAZIL_TZ) -> str:
        return dt.astimezone(ZoneInfo(tz)).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def from_date_and_time(date_str: str, time_str: str, tz: str = BRAZIL_TZ) -> datetime:
        dt = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
        return dt.replace(tzinfo=ZoneInfo(tz))
