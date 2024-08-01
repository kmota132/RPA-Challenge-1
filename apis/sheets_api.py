import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/drive"
]
SAMPLE_SPREADSHEET_ID = "1TGWBWTxmjTHWrMpfy9XS56uREx688cjFLlCL-2gP4a8"
SAMPLE_RANGE_NAME = "Sheet1!A2:N764"


class GSheetService:
    def authenticate(self):
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    def get_spreadsheet_data(self, creds):
        try:
            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
                .execute()
            )
            valores = result.get('values')

            if valores:
                data = []
                for linha in valores:
                    nome_empresa = linha[0]
                    cidade = linha[8]
                    deal_id = linha[10]
                    data.append((nome_empresa, cidade, deal_id))

                return data
            else:
                print("No data found.")
                return []

        except HttpError as err:
            print(err)
            return []


    def Uptade_Values(self, creds):
        try:
            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()

            updates = []
            range_name = "Sheet1!N2:N"

            result = (
                sheet.values()
                .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name)
                .execute()
            )
            values = result.get("values", [])

            new_values = [["YES"] for _ in range(len(values))]

            update_body = {"values": new_values}

            update_result = (
                sheet.values()
                .update(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    range=range_name,
                    valueInputOption="RAW",
                    body=update_body,
                )
                .execute()
            )

            print(f"{update_result.get('updatedCells')} células atualizadas com 'YES'.")

        except HttpError as err:
            print(err)

def main():
    gs_service = GSheetService()
    creds = gs_service.authenticate()
    if creds:
        data = gs_service.get_spreadsheet_data(creds)
        if data:
            return data
    return []


if __name__ == "__main__":
    gs_service = GSheetService()
    creds = gs_service.authenticate()
    if creds:
        data = gs_service.get_spreadsheet_data(creds)
        if data:
            gs_service.Uptade_Values(creds)


