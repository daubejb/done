import os
import os.path
import fcntl
import termios
import struct
import argparse
import webbrowser

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from colorama import init
from colorama import Fore
from colorama import Style

HISTORY_FILE = os.path.join(os.environ['HOME'], '.done_history.txt')
SPREADSHEET_ID = '1WIlw6BvlQtjXO9KtnT4b6XY8d3qAaK5RYDRnzekkVjM'
ACTIONS = ['action',
           'followup',
           'idea',
           'research',
           'schedule',
           'update']
CONTEXTS = ['work',
            'home']
WEB = 'https://docs.google.com/spreadsheets/d/%s' % (SPREADSHEET_ID)


def main():
    pass

class Terminal:
    '''Represents the terminal displays the user interface.'''
    def __init__(self):
        '''Initializes an instance of the terminal.'''

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
                                choices=['all', 'home', 'work'])
            parser.add_argument('--delete',
                                help='delete an item by id',
                                action='store',
                                dest='id_to_delete')
            parser.add_argument('-do', '--done',
                                help='mark an item as done by id',
                                action='store',
                                dest='id_done')
            parser.add_argument('-f', '--focus',
                                help='toggle focus mode - displays on today \
                                items',
                                action='store_true',
                                dest='focus')
            parser.add_argument('-g', '--group',
                                help='list only the items with the specified \
                                group',
                                action='store',
                                dest='group',
                                default='all',
                                choices=['action',
                                         'followup',
                                         'idea',
                                         'research',
                                         'schedule',
                                         'update'])
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
        if args.add:
            interactive_prompt = InteractivePrompt()
            inp = interactive_prompt.prompt_user_for_new_item()
            input_analyzer = InputAnalyzer()
            values = input_analyzer.break_item_string_into_parts(inp)
            return values, 'append_item'
        if args.web:
            webbrowser.open(WEB)
        if args.id_to_delete:
            return args.id_to_delete, 'delete_item'
        if args.id_done:
            print('do')
        if args.id_to_prioritize:
            print('priority')
        if args.id:
            print('move')


    def display_todo_list(self):
        '''displays the todo list in the terminal'''
        pass


class InteractivePrompt:
    '''Represents a dynamic fish shell like interaction with the user.'''
    def __init__(self):
        '''Initializes an instance of the interactive prompt'''

    def prompt_user_for_new_item(self):
        group_completer = WordCompleter(ACTIONS, ignore_case=True)
        inp = prompt('Enter to do item > ',
                     history=FileHistory(HISTORY_FILE),
                     auto_suggest=AutoSuggestFromHistory(),
                     completer=group_completer)
        return inp


class InputAnalyzer:
    '''Takes user input and parses it into distinct todo item fields'''
    def __init__(self):
        '''Initializes an input analyzer'''

    def break_item_string_into_parts(self, inp):
        '''Takes a string and breaks it up into the relavent to-do list
        parts'''
        self.inp = inp
        word_list = inp.split()
        first_word = word_list[0]
        last_word = word_list[-1]
        word_one = " "
        word_last = " "
        if first_word in ACTIONS:
            word_one = first_word
            del word_list[0]
        if last_word in CONTEXTS:
            word_last = last_word
            del word_list[-1]
        item_words = ' '.join(word_list)
        values = ['=row()-1', '', word_one, item_words, word_last]
        return values

if __name__ == '__main__':
    main()
