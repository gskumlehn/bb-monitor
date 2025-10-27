from typing import Dict, Any, List
from app.models.mention import Mention

class MentionService:

    def create_mention(self, data: Dict[str, Any]) -> Mention:
        return Mention(
            url=data.get("url"),
            original_url=data.get("originalUrl"),
            thread_url=data.get("threadURL"),
            title=data.get("title"),
            content=data.get("content"),
            author=data.get("author"),
            published_date=data.get("publishedDate"),
            sentiment=data.get("sentiment"),
            tags=data.get("tags", []),
        )

