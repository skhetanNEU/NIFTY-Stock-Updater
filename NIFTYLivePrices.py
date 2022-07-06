from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import requests

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

    dataFrame = pd.read_html(html_table.text)
    list_dataFrame = dataFrame[0].values.tolist()

    if(sheetName == 'NIFTY MidCap Live'):
        for current in list_dataFrame:
            current[0] = current[0].replace('  Add to Watchlist  Add to Portfolio','')

    # Call the Sheets API
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=sheetName + "!A2", valueInputOption="USER_ENTERED",
                                    body={"values": list_dataFrame})
    request.execute()

def RediffNIFTY(sheet):

    url = 'https://money.rediff.com/indices/nse/nifty-50'
    sheetName = "NIFTY 50 Live"

    FetchAndUpdate(url, sheetName, sheet)

def RediffNextNIFTY50(sheet):

    url = 'https://money.rediff.com/indices/nse/NIFTY-NEXT-50'
    sheetName = "Next NIFTY 50 Live"

    FetchAndUpdate(url, sheetName, sheet)

def NIFTYMidCapLive(sheet):

    #url = 'https://in.investing.com/indices/cnx-midcap-components'
    #url = 'https://www.icicidirect.com/equity/index/nse/nifty-midcap-100/26771'
    url = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=27'

    sheetName = "NIFTY MidCap Live"

    FetchAndUpdate(url, sheetName, sheet)

def StartUpdating():

    sheet = GetSheet()

    RediffNIFTY(sheet)
    RediffNextNIFTY50(sheet)
    NIFTYMidCapLive(sheet)

StartUpdating()