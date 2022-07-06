from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import requests
from bs4 import BeautifulSoup


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1MmHjJ4C2uNCBInG8Oz1hD0AvFBRqqNmdX4k0ceAgU-s'
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

def GetSheet():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'Keys.json'

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    return sheet

def FetchAndUpdate(url, sheetName, sheet):

  html_table = requests.get(url, headers=header)

  # fix HTML
  soup = BeautifulSoup(html_table.text, "html.parser")

  # warning - id results-table is your page specific
  for table in soup.findChildren(attrs={'id': 'results_table'}):
      for c in table.children:
          if c.name in ['tbody']:
              c.unwrap()

  dataFrame = pd.read_html(str(soup), flavor="bs4")
  list_dataFrame = dataFrame[0].values.tolist()

  # Call the Sheets API
  request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range=sheetName+"!A2", valueInputOption="USER_ENTERED", body={"values":list_dataFrame})
  request.execute()

def TopStockResearchNIFTY(sheet):
  url = 'https://www.topstockresearch.com/rt/IndexAnalyser/Nifty50/Technicals'
  sheetName = "NIFTY 50 Average"

  FetchAndUpdate(url, sheetName, sheet)

def TopStockResearchNextNIFTY50(sheet):
  url = 'https://www.topstockresearch.com/rt/IndexAnalyser/NiftyNext50/Technicals'
  sheetName = "Next NIFTY 50 Average"

  FetchAndUpdate(url, sheetName, sheet)

def TopStockResearchNIFTYMidCap(sheet):
  url = 'https://www.topstockresearch.com/rt/IndexAnalyser/NiftyMidCap100/Technicals'
  sheetName = "NIFTY MidCap Average"

  FetchAndUpdate(url, sheetName, sheet)

def UpdateAveragePrices():

    sheet = GetSheet()

    TopStockResearchNIFTYMidCap(sheet)
    TopStockResearchNextNIFTY50(sheet)
    TopStockResearchNIFTY(sheet)