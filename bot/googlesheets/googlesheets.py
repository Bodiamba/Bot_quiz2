from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleSheets:
    service_account_file: str
    spreadsheet_id: str
    range_column: str = 'A:C'

    def __init__(self, service_account_file: str, spreadsheet_id: str):
        self.service_account_file = service_account_file
        self.spreadsheet_id = spreadsheet_id

    async def set_data_to_google_sheets(self, list: list):
        """Записать данные. """
        VALUES_TO_WRITE = list
        # Список списков вида: [[name, str(score), datetime], ...]

        # Создаем credentials
        creds = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=['https://www.googleapis.com/auth/spreadsheets']
        )

        # Создаем сервис
        service = build('sheets', 'v4', credentials=creds)

        # Количество заполненных строк в указанном столбце
        result = service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=self.range_column).execute()
        values = result.get('values', [])
        last_row = len(values) if values else 0

        # Новый диапазон ячеек
        new_start_row = last_row + 1
        new_end_row = last_row + len(VALUES_TO_WRITE)
        new_range = f'Лист1!A{new_start_row}:C{new_end_row}'

        # Записываем данные
        body = {'values': VALUES_TO_WRITE}

        result = service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=new_range,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()