from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import settings

credentials = Credentials.from_service_account_file(
    settings.GOOGLE_CREDANTIONAL, scopes=settings.SCOPES
)


class SheetDriver:
    service = build("sheets", "v4", credentials=credentials)

    def __init__(self, spreadsheetId: str | None) -> None:
        self.spreadsheetId = spreadsheetId

    def append(self, values: list[list], range: str = "Лист1!A1"):

        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheetId,
            range=range,
            valueInputOption="USER_ENTERED",
            # insertDataOption="INSERT_ROWS",
            body={"values": values},
        ).execute()

        print(f"[INFO] Записано {len(values)} новых строк")

    def get(self, range: str = "A:W") -> list:
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheetId, range=range)
            .execute()
        )
        values = result.get("values", [])
        print(f"[INFO] Получено {len(values)}  строк")
        return values
