from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter


import fcntl
import termios
import struct
import argparse


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
        except ImportError:
            flags = None

    def display_todo_list():
        '''displays the todo list in the terminal'''
        pass

if __name__ == '__main__':
    main()
