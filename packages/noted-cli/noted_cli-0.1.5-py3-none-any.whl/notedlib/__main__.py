if __name__ == '__main__':
    import curses
    from notedlib.noted import Noted
    from notedlib.tui.tui import TUIApp
    from notedlib.exception import InvalidVaultKey, InvalidPasswordConfirmation

    try:
        with Noted() as api:
            tui = TUIApp(api)
            curses.wrapper(tui.main)
    except InvalidVaultKey as exc:
        print('Invalid vault key')
    except InvalidPasswordConfirmation as exc:
        print('Passwords didn\'t match')
