from enum import Enum


class AuthKeys(Enum):
    password_short = 'auth.password.too_short'
    password_long = 'auth.password.too_long'
    password_no_num = 'auth.password.no_number'
    password_no_upper = 'auth.password.no_upper'
    password_no_lower = 'auth.password.no_lower'
    missing_token = 'auth.missing_token'
    token_expired = 'auth.token_expired'
    no_privileges = 'auth.no_privileges'
    integrity_taken = 'auth.integrity_taken'
    invalid_password = 'auth.invalid_password'
    no_such_user = 'auth.no_such_user'
    not_owner = 'auth.not_owner'

    def __str__(self):
        return self.value
