from datetime import datetime
from zoneinfo import ZoneInfo
from app.infra.brandwatch_client import BrandwatchClient
import unittest

class TestBrandwatch(unittest.TestCase):

    def setUp(self):
        self.end_local = datetime(2025, 10, 16, 16, 30, tzinfo=ZoneInfo("America/Sao_Paulo"))
        self.start_local = datetime(2025, 10, 9, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo"))
        self.start_utc = self.start_local.astimezone(ZoneInfo("UTC"))
        self.end_utc = self.end_local.astimezone(ZoneInfo("UTC"))
        self.url = "https://g1.globo.com/mg/minas-gerais/noticia/2025/10/09/vereadores-de-bh-vao-ao-ccbb-com-guardas-e-pms-e-cobram-fechamento-de-exposicao.ghtml"

    def test_alerta_exemplo_brandwatch(self):
        print("==== Janela de busca (UTC) ====")
        print("start_utc:", self.start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))
        print("end_utc  :", self.end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))

        bw = BrandwatchClient()
        filters = {"url": self.url}
        mentions = bw.get_filtered_mentions(
            start_datetime=self.start_utc,
            end_datetime=self.end_utc,
            filters=filters,
            limit=500
        )

        print("\n--- LINK ---------------------------------------")
        print(self.url)
        self.assertTrue(mentions, "Nenhuma menção localizada para o alerta de exemplo no período informado.")

        exact = [m for m in mentions if m.get("url") == self.url or m.get("insightsUrl") == self.url]
        self.assertTrue(exact, "Nenhuma menção com a URL exata localizada no período informado.")

if __name__ == "__main__":
    unittest.main()
