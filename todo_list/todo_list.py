SPREADSHEET_ID = '1WIlw6BvlQtjXO9KtnT4b6XY8d3qAaK5RYDRnzekkVjM'
RANGE_ = '2done!A2:E1000'

class TodoList:
    '''Represents a minimal personal todo list containing to do items that
    can be added, done, deleted, and prioritized'''

    def __init__(self, name, ):
        '''Initialize a todo list with a name and an empty list'''
        self.name = name
        self.todo_items = []

    def add_item(self, item_id, today_flag, group, task, context):
        '''Create a new todo item and add it to the list'''
        self.todo_items.append(TodoItem(item_id, today_flag, group,
                                        task, context))

    # def find_item(self, column, value):
    #     '''Locate the todo item with the given id'''
    #     for todo_item in todo_items:
    #         if todo_item.id == item_id:
    #             return todo_item
    #     return None

    def populate_list(self, items):
        for item in items:
            item_id = item[0]
            today_flag = item[1]
            group = item[2]
            task = item[3]
            context = item[4]
            self.add_item(item_id, today_flag, group, task, context)
        return

    def filter_list_for_display(self, args, todo_list):
        context = args.context
        group = args.group
        filtered_list = []
        todo_items = todo_list.todo_items

        def build_row(item):
            row = [item.item_id,
                   item.today_flag,
                   item.group,
                   item.task,
                   item.context]
            return row
        # if settings['focus'] == True:
        #     for item in todo_items:
        #         if item.today_flag == 'yes':
        #             row = build_row(item)
        #             filtered_list.append(row)
        if group != 'all' and context != 'all':
            for item in todo_items:
                if item.group == group and item.context == context:
                    row = build_row(item)
                    filtered_list.append(row)
        elif group != 'all':
            for item in todo_items:
                if item.group == group:
                    row = build_row(item)
                    filtered_list.append(row)
        elif context != 'all':
            for item in todo_items:
                if item.context == context:
                    row = build_row(item)
                    filtered_list.append(row)
        else:
            for item in todo_items:
                row = build_row(item)
                filtered_list.append(row)
        return filtered_list


class TodoItem:
    '''Represents a todo item on the todo list.  Items have a unique id,
    task, an action type, a today flag used to focus on what is important, and
    a context (e.g., work or home)'''
    def __init__(self, item_id, today_flag, group, task, context):
        '''Initializes a todo item with a unique id, task, an optional
        action_type, context, and today flag'''
        self.task = task
        self.group = group
        self.today_flag = today_flag
        self.context = context
        self.item_id = item_id
