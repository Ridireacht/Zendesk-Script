import re
import gspread
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_URL

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Извлекаем ID Гугл-доки
def get_spreadsheet_id(url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if not match:
        raise ValueError("Неверный URL Google Sheet")
    return match.group(1)

# Авторизуемся в Google API и получаем себе Гугл-доку
def init_google(json_key):
    creds = Credentials.from_service_account_file(json_key, scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet_id = get_spreadsheet_id(SPREADSHEET_URL)
    spreadsheet = client.open_by_key(spreadsheet_id)
    return spreadsheet