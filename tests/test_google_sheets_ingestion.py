import unittest
import os
from dotenv import load_dotenv
from app.infra.google_sheets import GoogleSheets
from app.constants.ingestion_constants import IngestionConstants

class TestGoogleSheets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        credentials_path = f"../{os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
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
            "Enviado",
            "16/10/2025",
            "16:30",
            "Imprensa, Rede Social",
            "Nível 3",
            "Portal G1",
            "https://g1.globo.com/mg/minas-gerais/noticia/2025/10/09/vereadores-de-bh-vao-ao-ccbb-com-guardas-e-pms-e-cobram-fechamento-de-exposicao.ghtml",
            "“Vereadores de BH vão ao CCBB com guardas e PMs e cobram fechamento de exposição”",
            "Hoje (09), às 03h01, o portal G1 Minas Gerais que recebe 4 milhões de visitas/dia e com um alcance de 2.625 contas, publicou: “Vereadores de BH vão ao CCBB com guardas e PMs e cobram fechamento de exposição”. A exposição \"Fullgás\" traz obras que abordam o período do fim da ditadura militar. As alegadas cenas de nudez e sexo, são tidas como impróprias pelos parlamentares. \n\nNas redes sociais, às 06h51, o perfil no X Ricardo Carlini @carlinibh  tweetou: “Vereadores exigem reclassificação indicativa em exposição no CCBB”. A publicação, até o momento, possui 23 visualizações, com alcance de 11.822 contas e o perfil conta com pouco mais de 50 mil seguidores.\nOutro perfis como Itatiaia @Itatiaia também veicularam a notícia às 08h46 com o título: “CCBB BH se posiciona após vereadores acionarem a polícia para reclamar de exposição Clique e leia mais”. A publicação, até o momento, possui 1.618 visualizações, com alcance de 47.529 contas e o perfil conta com pouco mais de 1 milhão de seguidores.",
            "Tema crítico/sensível: Tema sociocultural/político envolvendo o CCBB.\nEmissor: Publicação por pelo menos um veículo relevante; Grupo de acessos A; Cita BB no título; Mega-influenciador ou celebridade; Perfil relevante ou Top Voice; Traz imagem ou vídeo associado ao BB.\nRepercussão: Tempo de exposição acima de 24h.",
            "Imprensa / Jornalistas\r\nAtores políticos / órgãos fiscalizadores",
            "07/10/2025 Nível 1\nNas redes sociais, hoje (08), às 16h31 o perfil @itatiaia(https://x.com/itatiaia/status/1976007616393511108) , publicou: \"Vereadores acionam a polícia e pedem interrupção de exposição no CCBB, em BH Clique e leia mais 👇. Junto ao link da matéria completa (https://www.itatiaia.com.br/cidades/vereadores-acionam-a-policia-e-pedem-interrupcao-de-exposicao-no-ccbb-em-bh) A publicação, até o momento, tem 514 visualizações e o perfil conta com um pouco mais de 1,2 milhões seguidores, com alcance até o momento de 47.529 contas."
        ]

        for i, value in enumerate(expected_first_row):
            with self.subTest(value=value):
                actual_value = self.result[1][i].strip()
                self.assertEqual(actual_value, value, rf"Valor da coluna {i + 1}: esperado '{value}', mas veio '{actual_value}'")

if __name__ == "__main__":
    unittest.main()
