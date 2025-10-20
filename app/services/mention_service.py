from typing import List, Dict, Any

class MentionService:

    def extract_categories_by_parent(mention: Dict[str, Any], parent_name: str) -> List[Dict[str, Any]]:
        category_details = mention.get("categoryDetails", [])
        return [
            category.name for category in category_details
            if category.get("parentName") == parent_name
        ]