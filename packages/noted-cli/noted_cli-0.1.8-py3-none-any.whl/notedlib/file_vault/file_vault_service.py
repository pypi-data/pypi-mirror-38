from os import path
from glob import glob
from pathlib import PurePath

from notedlib.encryption_service import EncryptionService
from notedlib.exception import InvalidVaultKey
from .protected_file import ProtectedFile, PROTECTED_FILE_EXTENSION
from .protected_file_cryptor import ProtectedFileCryptor

KEY_VERIFICATION_FILE_NAME = 'verification-key.enc'
KEY_VERIFICATION_CONTENT = b'SOME_RANDOM_CONTENT'  # TODO: really?


class FileVaultService:
    def __init__(self, directory: str, encryption_service: EncryptionService):
        self.directory = directory
        self.open_files = {}
        self.encryption_service = encryption_service
        self._try_verify_key()

    # PUBLIC API

    # The file will be imported and locked with the current key
    def import_file(self, id: str, source_path: str) -> None:
        protected_file = ProtectedFile(id, path.basename(source_path))
        protected_file_cryptor = self._create_protected_file_cryptor(
            protected_file)
        protected_file_cryptor.import_from_plain(source_path)

    def open_file(self, id: str, filename: str) -> ProtectedFileCryptor:
        if id in self.open_files:
            return self.open_files[id]

        protected_file = ProtectedFile(id, filename)
        protected_file_cryptor = self._create_protected_file_cryptor(
            protected_file)
        protected_file_cryptor.open()
        self.open_files[id] = protected_file_cryptor
        return protected_file_cryptor

    def close_file(self, id: str) -> None:
        protected_file_cryptor = self.open_files[id]
        protected_file_cryptor.close()
        del self.open_files[id]

    def close_opened(self):
        for id, protected_file_cryptor in self.open_files.items():
            protected_file_cryptor.close()

        self.open_files = {}

    # Delete encrypted file from vault
    def delete_file(self, id: str) -> None:
        protected_file_cryptor = self.open_files[id]
        protected_file_cryptor.delete()
        del self.open_files[id]

    # NOTE: This should not be run when database connection is open
    def change_key(self, new_key):
        self._open_all_encrypted_files()
        self.encryption_service.key = new_key
        self.close_opened()

    def _open_all_encrypted_files(self):
        ids = self._get_all_encrypted_file_ids()

        for id in ids:
            self.open_file(id, id + '.plain')

    # This function relies on the file naming convertion that ProtectedFile
    # provides
    # TODO: This can probably be cleaned up
    def _get_all_encrypted_file_ids(self):
        encrypted_files = glob(path.join(self.directory,
                                         '*.%s' % PROTECTED_FILE_EXTENSION))
        return [self._get_id_from_filename(filename)
                for filename in encrypted_files]

    def _get_id_from_filename(self, filename):
        return PurePath(filename).name.split('.')[0]

    def _create_protected_file_cryptor(
        self, protected_file: ProtectedFile
    ) -> ProtectedFileCryptor:
        return ProtectedFileCryptor(self.encryption_service, self.directory,
                                    protected_file)

    # KEY VERIFICATION

    def _try_verify_key(self) -> None:
        if not self._has_key_verification_file():
            self._create_key_verification_file()

        self._try_test_key_against_verification_file()

    def _has_key_verification_file(self) -> bool:
        return path.isfile(self._get_key_verification_file_path())

    def _create_key_verification_file(self):
        self.encryption_service.write_encrypted(
            self._get_key_verification_file_path(),
            KEY_VERIFICATION_CONTENT)

    def _get_key_verification_file_path(self) -> str:
        return path.join(self.directory, KEY_VERIFICATION_FILE_NAME)

    def _try_test_key_against_verification_file(self):
        plaintext = self.encryption_service.read_encrypted(
            self._get_key_verification_file_path())

        if plaintext != KEY_VERIFICATION_CONTENT:
            raise InvalidVaultKey('Invalid vault key')
