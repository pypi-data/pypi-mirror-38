from Crypto.Cipher import AES
from Crypto import Random
import base64

BS = AES.block_size
KEY_LENGTH = 32
KEY_PAD = '13a3b6b105ff48f5a1991df547794baf'


def pad(s):
    return s + bytes((BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf8')


def unpad(s):
    return s[:-ord(s[len(s)-1:])]


def padkey(key):
    if len(key) > 32:
        raise Exception('Key too long, AES can be 32 bytes long max')

    return key + KEY_PAD[0:KEY_LENGTH - len(key)]


class AESCipher:
    def __init__(self, key):
        self.key = padkey(key)

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(BS)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:BS]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[BS:]))
