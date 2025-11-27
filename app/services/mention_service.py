from typing import List, Dict, Any
from app.models.mention import Mention
from app.repositories.mention_repository import MentionRepository
from app.services.brandwatch_service import BrandwatchService
from app.enums.mention_category_parent_name import MentionCategoryParentName
from app.enums.mention_category_name import MentionCategoryName

class MentionService:

    def save_all(self, urls: List[str], datetime) -> List[Mention]:
        brandwatch_service = BrandwatchService()

        existing_mentions = MentionRepository.list_by_urls(urls)
        existing_urls = {m.url for m in existing_mentions}
        missing_urls = [url for url in urls if url not in existing_urls]

        mentions_data = brandwatch_service.fetch_mentions_by_urls_with_retry(urls=missing_urls, end_date=datetime)

        new_mentions = []
        for mention_data in mentions_data:
            mention = self.create(mention_data)
            saved_mention = MentionRepository.save(mention)
            new_mentions.append(saved_mention)

        return existing_mentions + new_mentions

    def create(self, data: Dict[str, Any]) -> Mention:
        mention = Mention()
        mention.url = data.get("url")

        filtered_categories = [
            category for category in data.get("categoryDetails", [])
            if category["parentName"] in [parent.value for parent in MentionCategoryParentName]
        ]

        mention.category_parent_names = [
            MentionCategoryParentName(category["parentName"])
            for category in filtered_categories
        ]

        mention.category_names = [
            MentionCategoryName(category["name"])
            for category in filtered_categories
        ]

        return mention