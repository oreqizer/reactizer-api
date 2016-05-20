from enum import Enum


class UserKeys(Enum):
    not_found = 'users.not_found'

    def __str__(self):
        return self.value
