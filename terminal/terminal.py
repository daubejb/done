import os
import os.path
import fcntl
import termios
import struct
import argparse
import webbrowser
import textwrap

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from terminaltables import AsciiTable
from colorama import init
from colorama import Fore
from colorama import Style


def main():
    pass


def get_ANSI_color(string):
    color = string
    color.upper()
    if color == 'GREEN':
        color = '\033[92m'
    elif color == 'RED':
        color = '\033[31m'
    elif color == 'YELLOW':
        color = '\033[93m'
    elif color == 'BLUE':
        color = '\033[34m'
    elif color == 'MAGENTA':
        color = '\033[95m'
    elif color == 'CYAN':
        color = '\033[36m'
    elif color == 'NORMAL':
        color = '\033[39m'
    elif color == 'WHITE':
        color = '\033[37m'
    return color


class Terminal:
    '''Represents the terminal displays the user interface.'''
    def __init__(self, app_conf):
        '''Initializes an instance of the terminal.'''
        self.application_name = app_conf.configs['application_name']
        self.spreadsheet_id = app_conf.configs['spreadsheet_id']
        self.today_color = get_ANSI_color(app_conf.configs['today_color'])
        self.header_row_color = get_ANSI_color(
            app_conf.configs['header_row_color'])
        self.history_location = app_conf.configs['history_file']
        self.history_file = os.path.join(
            os.environ[self.history_location], '.2done_history.txt')
        self.web = 'https://docs.google.com/spreadsheets/d/{}'.format(
            self.spreadsheet_id
        )
        self.actions = (app_conf.configs['actions']).split(',')
        self.contexts = (app_conf.configs['contexts']).split(',')
        self.display_lines = (
            app_conf.configs['display_lines_between_items'])
        self.display_list = (
            app_conf.configs['display_list_after_add_item'])

    def get_size(self):
        '''Analyzes the current terminal size and returns the width.'''
        th, tw, hp, wp = struct.unpack('HHHH',
                                       fcntl.ioctl(0, termios.TIOCGWINSZ,
                                                   struct.pack('HHHH',
                                                               0, 0, 0, 0)))
        return tw

    def get_user_input(self):
        '''Gets input from the user and performs the applicable action'''
        try:
            parser = argparse.ArgumentParser(description='a free and open \
                    source to do application accessible from anywhere')
            parser.add_argument('-a', '--add',
                                help='add an item to the list',
                                action='store_true',
                                dest='add')
            parser.add_argument('-c', '--context',
                                help='list only the items with the specified \
                                context',
                                action='store',
                                dest='context',
                                default='all',
                                choices=self.contexts)
            parser.add_argument('--delete',
                                help='delete an item by id',
                                action='store',
                                dest='id_to_delete')
            parser.add_argument('-do', '--done',
                                help='mark an item as done by id',
                                action='store',
                                dest='id_done')
            parser.add_argument('-f', '--focus',
                                help='display focus mode - displays on today \
                                items',
                                action='store_true',
                                dest='focus')
            parser.add_argument('-g', '--group',
                                help='list only the items with the specified \
                                group',
                                action='store',
                                dest='group',
                                default='all',
                                choices=self.actions)
            parser.add_argument('-m', '--move',
                                help='enter the id of the item you want to \
                                move and the destination position',
                                nargs=2,
                                dest='id',
                                action='store')
            parser.add_argument('-t', '--today',
                                help='toggle an item as important for today \
                                by id',
                                action='store',
                                dest='id_to_prioritize')
            parser.add_argument('-w', '--web',
                                help='open google sheet in a webbrowser',
                                action='store_true',
                                dest='web')
            args = parser.parse_args()
            return args
        except ImportError:
            flags = None

    def evaluate_user_input(self, args):
        if (args.add is False and
           args.id is None and
           args.id_done is None and
           args.id_to_delete is None and
           args.id_to_prioritize is None and
           not args.web):
            return args, 'display_list'
        if args.add:
            interactive_prompt = InteractivePrompt()
            inp = interactive_prompt.prompt_user_for_new_item(
                self.actions,
                self.history_file)
            input_analyzer = InputAnalyzer()
            values = input_analyzer.break_item_string_into_parts(
                inp, self.actions, self.contexts)
            return values, 'append_item'
        if args.web:
            webbrowser.open(self.web)
            quit()
        if args.id_to_delete:
            return args.id_to_delete, 'delete_item'
        if args.id_done:
            return args.id_done, 'done_item'
        if args.id_to_prioritize:
            return args.id_to_prioritize, 'prioritize_item'
        if args.id:
            return args.id, 'move_item'

    def display_todo_list(self, final_values):
        '''displays the todo list in the terminal'''
        term_width = self.get_size() - 30
        for row in final_values:
            total_length = len(row[0]) + len(row[1]) + len(row[2]) + \
                           len(row[3]) + len(row[4])
            other_columns = len(row[0]) + len(row[1]) + len(row[2]) + \
                len(row[4])
            short_length = term_width - other_columns
            if(total_length > term_width):
                shortened_text = textwrap.fill(row[3], width=short_length)
                row[3] = shortened_text
            yes = ['YES', 'Yes', 'yes', 'Y', 'y']
            if row[1] in yes:
                row[0] = self.today_color + row[0]
                row[4] = row[4] + Style.RESET_ALL

            data = []
            data.append([self.header_row_color +
                         Style.BRIGHT +
                         'id',
                         'today',
                         'group',
                         'todo item',
                         'context' +
                         Fore.RESET + Style.RESET_ALL])

            for row in final_values:
                data.append([row[0], row[1], row[2], row[3], row[4]])

        os.system('cls' if os.name == 'nt' else 'clear')
        table = AsciiTable(data)
        table.title = self.application_name
        print(table.table)


class InteractivePrompt:
    '''Represents a dynamic fish shell like interaction with the user.'''
    def __init__(self):
        '''Initializes an instance of the interactive prompt'''

    def prompt_user_for_new_item(self, actions, history):
        group_completer = WordCompleter(actions, ignore_case=True)
        inp = prompt('Enter to do item > ',
                     history=FileHistory(history),
                     auto_suggest=AutoSuggestFromHistory(),
                     completer=group_completer)
        return inp


class InputAnalyzer:
    '''Takes user input and parses it into distinct todo item fields'''
    def __init__(self):
        '''Initializes an input analyzer'''

    def break_item_string_into_parts(self, inp, actions, contexts):
        '''Takes a string and breaks it up into the relavent to-do list
        parts'''
        self.inp = inp
        word_list = inp.split()
        first_word = word_list[0]
        last_word = word_list[-1]
        word_one = " "
        word_last = " "
        if first_word in actions:
            word_one = first_word
            del word_list[0]
        if last_word in contexts:
            word_last = last_word
            del word_list[-1]
        item_words = ' '.join(word_list)
        values = ['=row()-1', '', word_one, item_words, word_last]
        return values

if __name__ == '__main__':
    main()
