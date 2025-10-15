import unittest
import os
from app.infra.google_sheets import GoogleSheets
from dotenv import load_dotenv


class TestGoogleSheets(unittest.TestCase):
    def setUp(self):
        load_dotenv()  # Carregar variáveis de ambiente do arquivo .env

        # Ajustar o caminho das credenciais para ser relativo à pasta do teste
        self.credentials_path = f"../{os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

        # Configurar os parâmetros do teste
        self.spreadsheet_id = "13Jjkl0AlYEEm0xryPL6PvdWYmkXN_a2qvl7h7GmEKUk"
        self.sheet_name = "oi"

    def test_fetch_data_real(self):
        # Dados esperados do Google Sheets
        expected_data = [
            ["nome", "genero"],
            ["lari", "fem"],
            ["pipo", "masc"],
            ["gk", "marmitex"]
        ]

        # Instanciar a infraestrutura e buscar os dados
        infra = GoogleSheets()
        range_name = f"{self.sheet_name}!A1:B4"
        result = infra.get_sheet_data(self.spreadsheet_id, range_name)

        # Verificar se os dados retornados correspondem aos dados esperados
        self.assertEqual(result, expected_data)

if __name__ == "__main__":
    unittest.main()
