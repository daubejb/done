from todo_list.todo_list import TodoList
from terminal.terminal import Terminal
from interface.api import GoogleAPI

def main():
    google_api = GoogleAPI()
    credentials = google_api.get_credentials()
    service = google_api.instantiate_api_service(credentials)
    terminal = Terminal()
    args = terminal.get_user_input()
    todo_list = TodoList('done')
    values = terminal.evaluate_user_input(args)
    print(values)
    all_list_data = todo_list.get_list_data(service)
    print(all_list_data)


if __name__ == '__main__':
    main()
