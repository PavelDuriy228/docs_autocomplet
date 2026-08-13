from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = Credentials.from_service_account_file(
    "encoded-might-505019-i9-62e1aa68b4c7.json", scopes=SCOPES
)

service = build("sheets", "v4", credentials=credentials)


SPREADSHEET_ID = "1xwg2HHC-RzswutMIKR44ZDYH1aQ6UCts0RDc8y6xk5s"

result = (
    service.spreadsheets()
    .values()
    .get(spreadsheetId=SPREADSHEET_ID, range="A1:R8")
    .execute()
)

rows = result.get("values", [])

for row in rows:
    print(row)
