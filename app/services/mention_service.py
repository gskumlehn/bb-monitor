from typing import Dict, Any, List
from app.models.mention import Mention
from app.repositories.mention_repository import MentionRepository
from app.services.brandwatch_service import BrandwatchService
from app.models.alert import Alert

class MentionService:

    def save(self, alert: Alert) -> List[Mention]:
        brandwatch_service = BrandwatchService()

        mentions = MentionRepository.find_by_alert_id(alert.id) or []
        if len(mentions) == len(alert.urls):
            return mentions

        missing_mention_urls = [u for u in alert.urls if u not in {m.url for m in mentions}]

        mentions_data = brandwatch_service.fetch_mentions_by_urls_with_retry(
            urls=missing_mention_urls,
            end_date=alert.delivery_datetime
        ) or []

        for url in missing_mention_urls:
            mention = self.create({
                "alert_id": alert.id,
                "id": next((m["brandwatch_id"] for m in mentions_data if m["url"] == url), None),
                "url": url,
            })
            saved = MentionRepository.save(mention)
            mentions.append(saved)

        return mentions

    def create(self, data: Dict[str, Any]) -> Mention:
        mention = Mention()
        mention.id = data.get("id")
        mention.alert_id = data.get("alert_id")
        mention.url = data.get("url")

        return mention