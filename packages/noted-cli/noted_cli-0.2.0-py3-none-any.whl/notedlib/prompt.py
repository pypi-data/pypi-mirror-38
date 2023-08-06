from getpass import getpass
from notedlib.exception import InvalidPasswordConfirmation


def ask_for_pw(message, confirm=False):
    password = getpass(message + ': ')

    if confirm:
        if getpass('Repeat again: ') != password:
            raise InvalidPasswordConfirmation('Passwords didn\'t match')

    return password
