from re import search


def check_password(password):
    # password too long
    if len(password) > 32:
        raise ValueError('auth.password.too_long')

    # password too short
    if len(password) < 8:
        raise ValueError('auth.password.too_short')

    # no number in password
    if not search(r'\d', password):
        raise ValueError('auth.password.no_number')

    # no uppercase letter in password
    if not search(r'\p{Lu}', password):
        raise ValueError('auth.password.no_uppercase')

    # no lowercase letter in password
    if not search(r'\p{Ll}', password):
        raise ValueError('auth.password.no_lowercase')
