import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import configparser

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Parse information from config.ini file
spreadsheets = config.get('Google API', 'spreadsheet')
subsheetname = config.get('Google API', 'subsheet_name')
api_url = config.get('Bitwarden', 'api_url')
master_password = config.get('Bitwarden', 'master_password')
folder_id = config.get('Bitwarden', 'folder_id')  
print("Successfully authenticated with Sheets API keys")

# Authenticate with Google Sheets API
json_keyfile_path = r'Path_to_Google_API_Json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path)
gc = gspread.authorize(credentials)

# Get the sub-sheet by name
try:
    spreadsheet = gc.open(spreadsheets)
    sheet = spreadsheet.worksheet(subsheetname)
    print(f"Successfully opened sub-sheet '{subsheetname}' in Google Sheet '{spreadsheets}'")
except gspread.exceptions.WorksheetNotFound:
    print(f"Sub-sheet '{subsheetname}' not found in Google Sheet '{spreadsheets}'.")

# Unlock the Bitwarden vault
def unlock_vault(master_password):
    unlock_data = {"password": master_password}
    response = requests.post(api_url + '/unlock', json=unlock_data)
    if response.status_code == 200:
        print("Vault unlocked successfully.")
        return True
    else:
        print("Failed to unlock the vault.")
        return False

# Function for creating or updating items in Bitwarden
def create_or_update_item(username, password, folder_id=None):
    # Construct the request body
    item_data = {
        'type': 1,
        'name': username,
        'notes': None,
        'favorite': False,
        'fields': [{'name': 'password', 'value': password}],
        'login': {'uris': [], 'username': username, 'password': password, 'totp': None},
        'reprompt': 0,
        'folderId': folder_id  
    }
    # Post Request to Import Usersnames and Passwords to the Bitwarden Folder of your choice
    try:
        response = requests.post(api_url + '/object/item', json=item_data)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        print(f"Imported {username} into Bitwarden.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to import {username} into Bitwarden. Error: {e}")

# Unlock the vault
if unlock_vault(master_password):
    # Add logging for each row processed
    for row in sheet.get_all_records():
        print("Processing row:", row)
        username = row['Username']
        password = row['Password']
        create_or_update_item(username, password, folder_id)  

    print("Script execution completed.")
else:
    print("Script execution terminated due to vault unlocking failure.")
