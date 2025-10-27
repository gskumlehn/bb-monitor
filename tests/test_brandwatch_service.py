import unittest
from datetime import datetime
from app.services.brandwatch_service import BrandwatchService

class TestBrandwatchService(unittest.TestCase):
    def test_fetch_mention_by_url_with_retry(self):
        brandwatch_service = BrandwatchService()

        url = "https://g1.globo.com/ma/maranhao/noticia/2025/10/08/auxilio-emergencial-governo-notifica-26-mil-familias-no-ma-para-devolver-r-65-milhoes-recebidos-indevidamente.ghtml"
        end_date = datetime(2025, 10, 23)

        mention = brandwatch_service.fetch_mention_by_url_with_retry(
            url=url,
            end_date=end_date,
            max_days_back=30,
            interval=20
        )

        if mention:
            print(f"Mention encontrada: {mention}")
        else:
            print("Mention não encontrada.")

        self.assertIsNotNone(mention, "A mention não foi encontrada.")

if __name__ == "__main__":
    unittest.main()
