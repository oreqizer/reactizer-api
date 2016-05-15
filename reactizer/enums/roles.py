from functools import total_ordering
from enum import Enum


@total_ordering
class Role(Enum):
    user = 1
    provider = 2
    admin = 3
    master = 4

    def __gt__(self, other):
        return self.value > other.value
