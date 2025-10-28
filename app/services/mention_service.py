from typing import Dict, Any, List, Optional
from app.models.mention import Mention
from app.repositories.mention_repository import MentionRepository
from app.services.brandwatch_service import BrandwatchService
from app.models.alert import Alert

class MentionService:

    def save(self, alert: Alert) -> List[Mention]:
        brandwatch_service = BrandwatchService()

        mentions_data = brandwatch_service.fetch_mentions_by_urls_with_retry(
            urls=alert.urls,
            end_date=alert.delivery_datetime
        ) or []

        saved_mentions: List[Mention] = []
        for url in alert.urls:
            mention = self.create({
                "alert_id": alert.id,
                "id": next((m["brandwatch_id"] for m in mentions_data if m["url"] == url), None),
                "url": url,
            })
            saved = MentionRepository.save(mention)
            saved_mentions.append(saved)

        return saved_mentions

    def create(self, data: Dict[str, Any]) -> Mention:
        mention = Mention()
        mention.id = data.get("id")
        mention.alert_id = data.get("alert_id")
        mention.url = data.get("url")

        return mention