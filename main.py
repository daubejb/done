import os
import os.path

from todo_list.todo_list import TodoList
from terminal.terminal import Terminal
from interface.api import GoogleAPI
from config import AppConf
from functions import reset_args


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

    #  if user updates source data, reset args, and display new list
    elif app_conf.configs['display_list_after_add_item'] == 'True':
        args2 = reset_args(args)
        evaluation_response2, action_type2 = terminal.evaluate_user_input(
            args2)
        response2 = google_api.process_api_call(
            evaluation_response2, action_type2)
        todo_list.populate_list(response2)
        final_list2 = todo_list.filter_list_for_display(args2, todo_list)
        terminal.display_todo_list(final_list2)

if __name__ == '__main__':
    main()
