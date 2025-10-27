import unittest
from app.infra.google_sheets import GoogleSheets
from app.constants.ingestion_constants import IngestionConstants

class TestGoogleSheets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        google_sheets = GoogleSheets()
        dynamic_range = f"'{IngestionConstants.SHEET_NAME}'!{IngestionConstants.START_COL}1:{IngestionConstants.END_COL}2"
        cls.result = google_sheets.get_sheet_data(IngestionConstants.SPREADSHEET_ID, dynamic_range)

    def setUp(self):
        self.result = self.__class__.result

    def test_collect_two_rows_and_store(self):
        self.assertGreaterEqual(len(self.result), 2, "A planilha deve retornar ao menos 2 linhas (cabeçalho + 1 linha de dados)")

    def test_header_matches_constants(self):
        for i, column in enumerate(IngestionConstants.EXPECTED_COLUMNS):
            with self.subTest(column=column):
                actual_column = self.result[0][i].strip()
                self.assertEqual(actual_column, column, rf"Coluna {i + 1}: esperado '{column}', mas veio '{actual_column}'")

    def test_first_row_matches_expected(self):
        expected_first_row = [
            "SIM",
            "1/10/2025",
            "08:55",
            "Rede Social",
            "@EInvestidor",
            "https://x.com/EInvestidor/status/1973329546863644676",
            "Hoje de manhã, (01) às 07h10, o perfil de E-Investidor @EInvestidor, (https://x.com/EInvestidor/status/1973329546863644676?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E1973329546863644676%7Ctwgr%5E011dedc8c55992bb9e377e52c0f21464bc90331d%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fapp.brandwatch.com%2Fproject%2F1998335642%2Fdashboards%2F1909249 )  tweetou: BB Seguridade (BBSE3): Ativa reduz preço-alvo da ação; veja motivos. Até o momento a publicação tem 244 visualizações e a página conta com 107.300 seguidores.",
            "Nas redes sociais, hoje de manhã (01) às 05h40, o perfil de E-Investidor @EInvestidor, (https://x.com/EInvestidor/status/1973306897466814871?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E1973306897466814871%7Ctwgr%5E011dedc8c55992bb9e377e52c0f21464bc90331d%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fapp.brandwatch.com%2Fproject%2F1998335642%2Fdashboards%2F1909249 )  tweetou: Quando o Banco do Brasil (BBAS3) voltará a pagar dividendos generosos? Empresa traça plano e analistas projetam prazo. Até o momento a publicação tem 429 visualizações e a página conta com 107.300 seguidores. NÍVEL DE CRITICIDADE: 0",
            "Nível 1",
            "Micro-Influenciador, Macro-Influenciador, >= 1 veículo relevante, Grupo B, Cita BB no Título, Publicador de Nicho",
            "Imprensa/Jornalistas",
            "Variáveis envolvidas:\nTema sensível: rebaixamento de preço-alvo de BBSE3 (impacto de mercado).\nEmissor/Meio: E-Investidor (mídia setorial de finanças; publicação em X/Twitter).\nEngajamento: 244 visualizações.\nAudiência do portal: 2.000.000 acessos/mês.\n"
        ]

        for i, value in enumerate(expected_first_row):
            with self.subTest(value=value):
                actual_value = self.result[1][i].strip()
                self.assertEqual(actual_value, value, rf"Valor da coluna {i + 1}: esperado '{value}', mas veio '{actual_value}'")

if __name__ == "__main__":
    unittest.main()
