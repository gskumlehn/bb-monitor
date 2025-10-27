import unittest
from datetime import datetime
from app.services.mention_service import MentionService

class TestMentionService(unittest.TestCase):
    def test_fetch_mention_by_url(self):
        # Instanciar o MentionService
        mention_service = MentionService()

        # Chamar o método fetch_mention_by_url com uma URL real
        url = "https://g1.globo.com/ma/maranhao/noticia/2025/10/08/auxilio-emergencial-governo-notifica-26-mil-familias-no-ma-para-devolver-r-65-milhoes-recebidos-indevidamente.ghtml"
        end_date = datetime(2025, 10, 23)

        # Realizar a busca
        mention = mention_service.fetch_mention_by_url(url=url, end_date=end_date, days_back=7)

        # Verificar se a menção foi encontrada
        if mention:
            print(f"Mention encontrada: {mention}")
        else:
            print("Mention não encontrada.")

        # Assert para garantir que o teste seja válido
        self.assertIsNotNone(mention, "A mention não foi encontrada.")

if __name__ == "__main__":
    unittest.main()
