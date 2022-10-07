from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

# Repo With Hash
COL_CHECKED = 0
COL_REPO = 1
COL_HASH = 2
COL_TEST_FRAMEWORK = 3
COL_COMPLETED = 4
COL_TIME = 5
COL_SCG = 6
COL_DCG = 7
COL_SM = 8
COL_DM = 9
COL_INJECT = 10
COL_NOTE = 11

# Mapping
MCOL_CHECKED = 0
MCOL_REPO = 1
MCOL_HASH = 2
MCOL_TEST_FRAMEWORK = 3
MCOL_COMPLETED = 4
MCOL_TIME = 5
MCOL_SCG = 6
MCOL_DCG = 7
MCOL_SM = 8
MCOL_DM = 9
MCOL_MAP = 10
MCOL_GENERATED = 11
MCOL_NOTE = 12


class SheetException(Exception):
    def __init__(self, message):
        super().__init__(self, message)


class Sheets:
    def __init__(self, file, spreadsheet_id, input_worksheet, output_worksheet):
        self.file = file
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = self.init_creds()
        self.service = self.init_service()
        self.sheet = self.init_sheet()
        self.spreadsheet_id = spreadsheet_id
        self.input_worksheet = input_worksheet
        self.output_worksheet = output_worksheet

    def init_creds(self):
        if os.path.exists(self.file):
            return service_account.Credentials.from_service_account_file(self.file, scopes=self.scopes)
        else:
            raise SheetException(f"Credential error: key file '{self.file}' doesn't exist")

    def init_service(self):
        if self.creds is not None:
            return build('sheets', 'v4', credentials=self.creds)
        else:
            raise SheetException(f"Service error: credentials are not initialized properly!")

    def init_sheet(self):
        if self.service is not None:
            return self.service.spreadsheets()
        else:
            raise SheetException(f"Spreadsheet error: service is not initialized properly!")

    def clear(self, area):
        request = self.sheet.values().clear(spreadsheetId=self.spreadsheet_id, range=f"{self.output_worksheet}!{area}")
        return request.execute()

    def push(self, values, column):
        request = self.sheet.values().update(spreadsheetId=self.spreadsheet_id,
                                             range=f"{self.output_worksheet}!A{column}",
                                             valueInputOption="USER_ENTERED",
                                             body={"values": values})

        return request.execute()

    def push_running(self, values):
        request = self.sheet.values().append(spreadsheetId=self.spreadsheet_id,
                                             range=f"{self.output_worksheet}!A2",
                                             valueInputOption="USER_ENTERED",
                                             body={"values": values})
        return request.execute()

    def get_modules(self):
        def module(row):
            result = {
                "name": row[COL_REPO].split("/")[-2],
                "repo": row[COL_REPO][:-1] + ".git",
                "hash": row[COL_HASH],
                "testing-framework": row[COL_TEST_FRAMEWORK],
                "inject": row[COL_INJECT].split(", ")
            }
            return result

        request = self.sheet.values().get(spreadsheetId=self.spreadsheet_id, range=f"{self.input_worksheet}!A2:K99")
        respond = request.execute()

        modules = []

        values = respond.get('values', [])
        for row in values:
            if row[COL_CHECKED] == 'TRUE':
                modules.append(module(row))

        return modules

    def mapping_data(self):
        def module(row, row_number):
            result = {
                "line": row_number,
                "tick": row[MCOL_CHECKED],
                "name": row[MCOL_REPO].split("/")[-2],
                "repo": row[MCOL_REPO],
                "hash": row[MCOL_HASH],
                "completed": row[MCOL_COMPLETED],
                "time": row[MCOL_TIME],
                "testing-framework": row[MCOL_TEST_FRAMEWORK],
                "SCG": row[MCOL_SCG],
                "DCG": row[MCOL_DCG],
                "SM": row[MCOL_SM],
                "DM": row[MCOL_DM],
                "Map": row[MCOL_MAP],
                "Note": row[MCOL_NOTE],
                "Generated": '',
            }
            return result

        request = self.sheet.values().get(spreadsheetId=self.spreadsheet_id, range=f"{self.input_worksheet}!A2:M99")
        respond = request.execute()

        modules = []

        row_number = 2

        values = respond.get('values', [])
        for row in values:
            if row[MCOL_CHECKED] == 'TRUE':
                modules.append(module(row, row_number))

            row_number += 1

        return modules

# GET EXAMPLE
# sheet.values().get(spreadsheetId=SPREADSHEET_ID,range="Hca-results")\
#     .execute()
# result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                             range="Hca-results").execute()
# values = result.get('values', [])
# for i in values:
#     print(i)


# repo_data = [
#     ["https://github.com/mysqljs/mysql/", "urun", "Yes", "-", "-", "index + test**", ":)"],
#     ["https://github.com/juliangruber/brace-expansion/", "Tape", "Yes", "No", "No", "index + test**", "Can't compare: [Anyonymus] | No callgraph"],
# ]
