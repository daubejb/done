import os
import os.path
import time
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = '2done'
RANGE = '2done!A2:E1000'
DONE_RANGE = 'done!A2:F1000'
SPREADSHEET_ID = '1WIlw6BvlQtjXO9KtnT4b6XY8d3qAaK5RYDRnzekkVjM'


class GoogleAPI:
    '''Represents the v4 google api for interacting with google apps'''

    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   CLIENT_SECRET_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', credentials=credentials)
    print(service)
    def __init__(self):
        '''Instantiates a google api'''

    def process_api_call(self, values, action_type):
        '''Receives an api request and processes it based on the arguments.'''
        if action_type == 'append_item':
            self.append_item_to_sheet(values)
        if action_type == 'delete_item':
            self.delete_item_from_sheet(values)
        if action_type == 'done_item':
            self.done_item_from_sheet(values)
        if action_type == 'prioritize_item':
            self.toggle_item_priority(values)
        if action_type == 'move_item':
            self.move_item_to_new_position(values)


    def append_item_to_sheet(self, values):
        body = {
            "range": RANGE,
            "majorDimension": 'ROWS',
            "values": [
                values
            ],
        }
        s = self.service
        s.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range=RANGE,
            valueInputOption='USER_ENTERED',
            body=body).execute()

    def delete_item_from_sheet(self, item_id):
        item_id = int(item_id)
        startIndex = item_id
        endIndex = item_id + 1
        batch_update_values_request_body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": 0,
                            "dimension": "ROWS",
                            "startIndex": startIndex,
                            "endIndex": endIndex
                        }
                    }
                }
            ]
        }
        s = self.service
        request = s.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=batch_update_values_request_body)
        response = request.execute()
        print(response)
        if 'replies' in response and 'spreadsheetId' in response:
            print('Item # %s deleted from list' % id)

    def done_item_from_sheet(self, item_id):
        item_id = int(item_id)
        A1 = item_id + 1
        ranges = ['%s!A%s:E%s' % (APPLICATION_NAME, A1, A1)]
        s = self.service
        request = s.spreadsheets().values().batchGet(
                spreadsheetId=SPREADSHEET_ID,
                ranges=ranges,
                valueRenderOption='UNFORMATTED_VALUE',
                dateTimeRenderOption='FORMATTED_STRING')

        response = request.execute()

        values = response['valueRanges'][0]['values'][0]
        values[0] = '=row()-1'
        values.insert(len(values), time.strftime("%Y-%m-%d"))
        body = {
                "range": DONE_RANGE,
                "majorDimension": 'ROWS',
                "values": [
                        values
                    ],
        }
        result = s.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range=DONE_RANGE,
            valueInputOption='USER_ENTERED',
            body=body).execute()
        self.delete_item_from_sheet(item_id)
        return

    def toggle_item_priority(self, item_id):
        item_id = int(item_id)
        A1 = item_id + 1
        print(id)
        print(A1)
        range_ = '%s!B%s' % (APPLICATION_NAME, A1)
        s = self.service
        request = s.spreadsheets().values().batchGet(
                spreadsheetId=SPREADSHEET_ID,
                ranges=range_,
                valueRenderOption='FORMATTED_VALUE',
                dateTimeRenderOption='FORMATTED_STRING')

        response = request.execute()

        if 'values' not in response['valueRanges'][0]:
            priority = "yes"
        else:
            priority = response['valueRanges'][0]['values'][0]
            if priority[0] == 'Yes' or priority[0] == 'yes':
                priority = " "
            else:
                priority = 'yes'

        value_input_option = 'USER_ENTERED'

        body_ = {
            "values": [
                [priority]
                ]
            }

        request = s.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_,
                valueInputOption=value_input_option,
                includeValuesInResponse=True,
                body=body_)
        response = request.execute()
        return

    def move_item_to_new_position(self, item_ids):
        destination_row_index = int(item_ids[1])
        item_to_move = int(item_ids[0])
        end_index = item_to_move + 1
        batch_update_spreadsheet_request_body = {
                'requests': [
                    {
                        "moveDimension": {
                            "source": {
                                "sheetId": 0,
                                "dimension": "ROWS",
                                "startIndex": item_to_move,
                                "endIndex": end_index
                                },
                            "destinationIndex": destination_row_index
                            }
                        },
                    ]
                }
        s = self.service
        request = s.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=batch_update_spreadsheet_request_body)
        response = request.execute()