from todo_list.todo_list import TodoList
from terminal.terminal import Terminal
from interface.api import GoogleAPI

def main():
    terminal = Terminal()
    args = terminal.get_user_input()
    todo_list = TodoList('done')
    google_api = GoogleAPI()
#    credentials = google_api.get_credentials()
#    service = google_api.instantiate_api_service(credentials)
    values = terminal.evaluate_user_input(args)
    google_api.process_api_call(values, 'append_item')
    

if __name__ == '__main__':
    main()
