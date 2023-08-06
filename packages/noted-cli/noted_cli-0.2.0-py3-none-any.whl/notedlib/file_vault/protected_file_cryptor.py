from os import path
from hashlib import sha256
from notedlib.storage import shred_file, get_file_checksum, create_temp_file
from notedlib.encryption_service import EncryptionService
from .protected_file import ProtectedFile


class ProtectedFileCryptor:
    def __init__(self, encryption_service: EncryptionService, directory: str,
                 protected_file: ProtectedFile):
        self.encryption_service = encryption_service
        self.directory = directory
        self.protected_file = protected_file
        self.file_checksum_on_open = None
        self.key_checksum_on_open = None
        self._temp_access_path = None

    @property
    def encrypted_file_path(self) -> str:
        return path.join(self.directory, self.protected_file.encrypted_name)

    @property
    def temp_access_path(self) -> str:
        if not self._temp_access_path:
            self._temp_access_path = self._create_new_temp_access_path()

        return self._temp_access_path

    def open(self) -> str:
        plain = self.encryption_service.read_encrypted(
            self.encrypted_file_path)
        self.encryption_service.write_plain(
            self.temp_access_path,
            plain)
        self.file_checksum_on_open = get_file_checksum(self.temp_access_path)
        self.key_checksum_on_open = self._get_encryption_key_hash()
        return self.temp_access_path

    def _create_new_temp_access_path(self) -> str:
        return create_temp_file(self.protected_file.original_name)

    def close(self) -> None:
        if self._is_file_changed_since_open() or self._is_key_changed_since_open():
            self.import_from_plain(self.temp_access_path)

        shred_file(self.temp_access_path)

    def _is_file_changed_since_open(self) -> bool:
        return self.file_checksum_on_open != get_file_checksum(self.temp_access_path)

    def _is_key_changed_since_open(self) -> bool:
        return self._get_encryption_key_hash() != self.key_checksum_on_open

    def _get_encryption_key_hash(self):
        return sha256(self.encryption_service.key.encode('utf8'))

    def import_from_plain(self, source_path: str) -> None:
        plain = self.encryption_service.read_plain(source_path)
        self.encryption_service.write_encrypted(
            self.encrypted_file_path, plain)

    # TODO: check if files exists first?
    def delete(self) -> None:
        shred_file(self.temp_access_path)
        shred_file(self.encrypted_file_path)

    def __repr__(self) -> str:
        return '%s(protected_file=%s, temp_access_path=%s)' % (
            self.__class__.__name__,
            repr(self.protected_file),
            self._temp_access_path)
