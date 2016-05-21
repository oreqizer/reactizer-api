from enum import Enum


class TodoKeys(Enum):
    not_owner = 'todos.not_owner'
    not_found = 'todos.not_found'

    def __str__(self):
        return self.value
