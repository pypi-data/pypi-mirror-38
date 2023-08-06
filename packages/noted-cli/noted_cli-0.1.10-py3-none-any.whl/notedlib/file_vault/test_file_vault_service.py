import unittest
from os import mkdir, listdir, path, remove
from shutil import rmtree

from notedlib.file_vault.file_vault_service import FileVaultService
from notedlib.encryption_service import EncryptionService
from notedlib.exception import InvalidVaultKey

TEST_VAULT_DIR_PATH = './test-vault-dir'
TEST_PLAINTEXT_FILE_PATH = './test-plaintext-file.txt'


class TestFileVaultService(unittest.TestCase):
    def setUp(self):
        self._setup_test_files()
        self.enc_service = EncryptionService('mypassphrase')
        self.vault = FileVaultService(TEST_VAULT_DIR_PATH, self.enc_service)

    def _setup_test_files(self):
        mkdir(TEST_VAULT_DIR_PATH)
        write_file(TEST_PLAINTEXT_FILE_PATH, 'This is some plain text')

    def tearDown(self):
        rmtree(TEST_VAULT_DIR_PATH)
        remove(TEST_PLAINTEXT_FILE_PATH)

    # Instantiation
    def test_instantiate_with_invalid_key_should_raise_error(self):
        enc_service = EncryptionService('thisIsTheWrongKey')
        self.assertRaises(InvalidVaultKey, FileVaultService,
                          TEST_VAULT_DIR_PATH, enc_service)

    # Import file
    def test_import_file_should_create_encrypted_version(self):
        self.vault.import_file('1', TEST_PLAINTEXT_FILE_PATH)
        assert is_directory_containing_files(TEST_VAULT_DIR_PATH, ['1.enc'])

    def test_import_file_should_leave_plain_untouched(self):
        contents_before = read_file(TEST_PLAINTEXT_FILE_PATH)
        self.vault.import_file('1', TEST_PLAINTEXT_FILE_PATH)
        contents_after = read_file(TEST_PLAINTEXT_FILE_PATH)
        assert contents_before == contents_after

    # Open file
    def test_open_file_should_make_plain_file_temporarily_available(self):
        self.vault.import_file('1', TEST_PLAINTEXT_FILE_PATH)
        file_encryptor = self.vault.open_file('1', 'test-plaintext-file.txt')
        plain_contents = read_file(file_encryptor.temp_access_path)
        assert plain_contents == 'This is some plain text'

    def test_open_file_should_not_open_already_opened_file(self):
        self.vault.import_file('1', TEST_PLAINTEXT_FILE_PATH)
        file_encryptor1 = self.vault.open_file('1', 'test-plaintext-file.txt')
        file_encryptor2 = self.vault.open_file('1', 'test-plaintext-file.txt')
        assert file_encryptor1 == file_encryptor2

    # Close file(s)
    def test_close_file_should_make_temporary_file_unavailable(self):
        self.vault.import_file('1', TEST_PLAINTEXT_FILE_PATH)
        file_encryptor = self.vault.open_file('1', 'test-plaintext-file.txt')
        temp_access_path = file_encryptor.temp_access_path
        assert path.isfile(temp_access_path)
        self.vault.close_file('1')
        assert not path.isfile(temp_access_path)

    def test_close_file_should_overwrite_existing_file_if_changed(self):
        self.vault.import_file('1', TEST_PLAINTEXT_FILE_PATH)
        file_encryptor = self.vault.open_file('1', 'test-plaintext-file.txt')
        encrypted_file_path = file_encryptor.encrypted_file_path
        encrypted_contents_before = read_file(encrypted_file_path)

        write_file(file_encryptor.temp_access_path, 'Updated contents')
        self.vault.close_file('1')

        encrypted_contents_after = read_file(encrypted_file_path)
        assert encrypted_contents_before != encrypted_contents_after

    def test_close_opened_files_should_close_all_opened_files(self):
        temp_access_paths = []

        for x in range(3):
            id = str(x)
            self.vault.import_file(id, TEST_PLAINTEXT_FILE_PATH)
            file_encryptor = self.vault.open_file(
                id, 'test-plaintext-file.txt')
            temp_access_paths.append(file_encryptor.temp_access_path)

        self.vault.close_opened()

        for temp_access_path in temp_access_paths:
            assert not path.isfile(temp_access_path)

    # Delete file
    def test_delete_file_should_remove_encrypted_version(self):
        self.vault.import_file('1', TEST_PLAINTEXT_FILE_PATH)
        file_encryptor = self.vault.open_file('1', 'test-plaintext-file.txt')
        encrypted_file_path = file_encryptor.encrypted_file_path

        self.vault.delete_file('1')

        assert not path.isfile(encrypted_file_path)

    # Change key
    def test_change_key_should_reencrypt_all_files_in_vault(self):
        # Import (encrypt file) with original key
        self.vault.import_file('1', TEST_PLAINTEXT_FILE_PATH)

        # Save file state before key change
        file_encryptor = self.vault.open_file('1', 'test-plaintext-file.txt')
        encrypted_file_path = file_encryptor.encrypted_file_path
        encrypted_file_contents_before = read_file(encrypted_file_path)

        # Change the key
        self.vault.change_key('new key!')
        self.vault.close_opened()  # Not needed, but increases readability

        # Compare file state after key change
        encrypted_file_contents_after = read_file(encrypted_file_path)
        assert encrypted_file_contents_before != encrypted_file_contents_after

        # Open file with new key and make sure that we can read the contents
        file_encryptor = self.vault.open_file('1', 'test-plaintext-file.txt')
        plaintext_after_key_change = read_file(file_encryptor.temp_access_path)
        assert plaintext_after_key_change == 'This is some plain text'


def is_directory_containing_files(directory, expected_files):
    found_files = set(listdir(directory))
    expected_files = set(expected_files)
    return expected_files.issubset(found_files)


def write_file(file_path, contents):
    with open(file_path, 'w') as writestream:
        writestream.write(contents)


def read_file(file_path):
    with open(file_path, 'r') as readstream:
        return readstream.read()


if __name__ == '__main__':
    unittest.main()
