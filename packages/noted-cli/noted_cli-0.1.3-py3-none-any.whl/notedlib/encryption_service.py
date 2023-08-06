from .helper.encryption import AESCipher


class EncryptionService:
    def __init__(self, key: str):
        self.key = key

    def read_plain(self, source_path: str) -> bytes:
        with open(source_path, 'rb') as readstream:
            return readstream.read()

    def write_plain(self, file_path: str, plain: bytes) -> None:
        with open(file_path, 'wb') as writestream:
            writestream.write(plain)

    def read_encrypted(self, source_path: str) -> bytes:
        return self.decrypt_bytes(self.read_plain(source_path))

    def write_encrypted(self, file_path: str, plain: bytes) -> None:
        self.write_plain(file_path, self.encrypt_bytes(plain))

    def encrypt_bytes(self, plain: bytes) -> bytes:
        cipher = AESCipher(self.key)
        return cipher.encrypt(plain)

    def decrypt_bytes(self, encrypted: bytes) -> bytes:
        cipher = AESCipher(self.key)
        return cipher.decrypt(encrypted)
