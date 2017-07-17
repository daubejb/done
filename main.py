from todo_list.todo_list import TodoList
from terminal.terminal import Terminal
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import os
import os.path


def get_credentials():
    # Gets valid user credentials from storage.
    # If nothing has been stored, or if the stored credentials are invalid,
    # the OAuth2 flow is completed to obtain the new credentials.
    # Returns:
    #     Credentials, the obtained credential.

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
            flags = tools.argparser.parse_args(args=[])
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def instantiate_api_service(credentials):
    http = credentials.authorize(httplib2.Http())
    # API Call
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service


def main():
    t = Terminal()
    t.get_user_input()

if __name__ == '__main__':
    main()
