from notedlib.storage import get_file_extension


PROTECTED_FILE_EXTENSION = 'enc'


class ProtectedFile:
    def __init__(self, id: str, original_name: str):
        self.id = id
        self.original_name = original_name

    @property
    def extension(self) -> str:
        return get_file_extension(self.original_name)

    @property
    def encrypted_name(self) -> str:
        return '%s.%s' % (self.id, PROTECTED_FILE_EXTENSION)

    def __repr__(self) -> str:
        return '%s(id=%s, original_name=%s)' % (self.__class__.__name__,
                                                self.id,
                                                self.original_name)
