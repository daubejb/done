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
    evaluation_response, action_type = terminal.evaluate_user_input(args)
    response = google_api.process_api_call(evaluation_response, action_type)
    if action_type == 'display_list':
        todo_list.populate_list(response)
        final_list = todo_list.filter_list_for_display(args, todo_list)
        terminal.display_todo_list(final_list)
if __name__ == '__main__':
    main()
