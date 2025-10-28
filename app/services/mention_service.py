from typing import Dict, Any, List
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
        )

        for mention_data in mentions_data:
            mention = self.create({
                "alert_id": alert.id,
                "id": mention_data.get("brandwatch_id"),
                "url": mention_data["url"],
            })

            MentionRepository.save(mention)


    def create(self, data: Dict[str, Any]) -> Mention:
        mention = Mention()

        mention.id = data.get("id")
        mention.alert_id = data.get("alert_id")
        mention.url = data.get("url")

        return mention