#!/usr/bin/env python3
import curses
from notedlib.noted import Noted
from notedlib.tui.tui import TUIApp
from notedlib.exception import InvalidVaultKey, InvalidPasswordConfirmation


def tui():
    try:
        with Noted() as api:
            tui = TUIApp(api)
            curses.wrapper(tui.main)
    except InvalidVaultKey as exc:
        print('Invalid vault key')
    except InvalidPasswordConfirmation as exc:
        print('Passwords didn\'t match')


def cli():
    print('TODO!')


if __name__ == '__main__':
    tui()
