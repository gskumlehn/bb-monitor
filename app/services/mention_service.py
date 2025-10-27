from typing import Dict, Any, List
from app.models.mention import Mention

class MentionService:
    def create_mention(self, data: Dict[str, Any]) -> Mention:
        """
        Cria uma instância do modelo Mention a partir dos dados fornecidos.
        """
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

    def create_mentions(self, data_list: List[Dict[str, Any]]) -> List[Mention]:
        """
        Cria uma lista de instâncias do modelo Mention a partir de uma lista de dados.
        """
        return [self.create_mention(data) for data in data_list]
