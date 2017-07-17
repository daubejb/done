class TodoList:
    '''Represents a minimal personal todo list containing to do items that
    can be added, done, deleted, and prioritized'''
    def __init__(self, name, ):
        '''Initialize a todo list with a name and an empty list'''
        self.name = name
        self.todo_items = []

    def add_item(self, task):
        '''Create a new todo item and add it to the list'''
        self.todo_items.append(TodoItem(task, action_type='', today_flag=False,
                                        context=''))

    def find_item(self, item_id):
        '''Locate the todo item with the given id'''
        for todo_item in todo_items:
            if todo_item.id == item_id:
                return todo_item
        return None

# Store the next available id for all new todo items
last_todo_id = 0


class TodoItem:
    '''Represents a todo item on the todo list.  Items have a unique id,
    task, an action type, a today flag used to focus on what is important, and
    a context (e.g., work or home)'''
    def __init__(self, task, action_type='', today_flag=False, context=''):
        '''Initializes a todo item with a unique id, task, an optional
        action_type, context, and today flag'''
        self.task = task
        self.action_type = action_type
        self.today_flag = today_flag
        self.context = context
        global last_todo_id
        last_todo_id += 1
        self.item_id = last_todo_id
