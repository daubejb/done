import os
import os.path

from todo_list.todo_list import TodoList
from terminal.terminal import Terminal
from interface.api import GoogleAPI
from config import AppConf


def main():
    # check for an existing configuration file
    app_conf = AppConf()

    #  use terminal to parse user input
    terminal = Terminal(app_conf)
    args = terminal.get_user_input()

    #  instantiate a todo list named done
    todo_list = TodoList('done')

    #  instantiate the google api object
    google_api = GoogleAPI()

    #  evaluate user intention and prepare the data for google api
    evaluation_response, action_type = terminal.evaluate_user_input(args)

    #  process the request to act on the google sheet via api
    response = google_api.process_api_call(evaluation_response, action_type)

    #  if user requests to see the to-do list, present what they request
    if action_type == 'display_list':
        todo_list.populate_list(response)
        final_list = todo_list.filter_list_for_display(args, todo_list)
        terminal.display_todo_list(final_list)
if __name__ == '__main__':
    main()
