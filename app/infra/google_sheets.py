import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

class GoogleSheets:

    def __init__(self):
        credentials = Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
        self.service = build("sheets", "v4", credentials=credentials)

    def get_sheet_data(self, spreadsheet_id, range_name):
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            return result.get("values", [])
        except Exception as e:
            raise RuntimeError(f"Erro ao consultar Google Sheets: {e}")

    def get_sheet_data_with_start_row(self, spreadsheet_id, dynamic_range):
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=dynamic_range).execute()
            return result.get("values", [])
        except Exception as e:
            raise RuntimeError(f"Erro ao consultar Google Sheets com linha inicial: {e}")
