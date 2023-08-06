# TODO: Rename exceptions (remove Exception)
class NotSetupException(Exception):
    pass


class NoSuchAdapterException(Exception):
    pass


class InvalidTagNameException(Exception):
    pass


class EnsureTagCreationException(Exception):
    pass


class ForbiddenSetterException(Exception):
    pass


class InvalidPasswordConfirmation(Exception):
    pass


class InvalidVaultKey(Exception):
    pass


class InvalidCommand(Exception):
    pass
