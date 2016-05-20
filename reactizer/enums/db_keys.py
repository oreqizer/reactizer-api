from enum import Enum


class DbKeys(Enum):
    protected_key = 'db.protected_key'

    def __str__(self):
        return self.value
