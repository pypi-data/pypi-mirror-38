import notedlib.storage as storage
import notedlib.database as database
import notedlib.migration as migration
from notedlib.tui.input import get_escape_delay, set_escape_delay
from .file_vault.file_vault_service import FileVaultService
from .encryption_service import EncryptionService
from .prompt import ask_for_pw
from .api import API


class Noted:
    def __init__(self, key=None):
        self.encryption_service = None
        self.vault = None
        self.initial_escape_delay = None

        if key:
            self._setup_vault(key)

    def __enter__(self):
        if self._is_first_use():
            self._install()
        elif not self.vault:
            key = ask_for_pw('Enter your encryption passphrase')
            self._setup_vault(key)

        self._handle_escape_delay()
        self._initialize_database_connection()
        return API()

    def _is_first_use(self):
        return not storage.directory_exists() or storage.is_empty()

    def _install(self):
        storage.ensure_directory_created()

        if not self.vault:
            key = ask_for_pw('Setup your encryption passphrase', True)
            self._setup_vault(key)

        temp_file = storage.create_temp_file('database.db')
        self.vault.import_file('database', temp_file)

    def _setup_vault(self, key):
        self.encryption_service = EncryptionService(key)
        self.vault = FileVaultService(
            storage.get_directory(), self.encryption_service)

    def _initialize_database_connection(self):
        database_file = self.vault.open_file('database', 'database.db')
        database.initialize_connection(database_file.temp_access_path)
        migration.migrate()

    def _handle_escape_delay(self):
        self._backup_escape_delay()
        set_escape_delay(0)

    def _backup_escape_delay(self):
        self.initial_escape_delay = get_escape_delay()

    def _restore_escape_delay(self):
        set_escape_delay(self.initial_escape_delay)

    def __exit__(self, exception_type, exception_value, traceback):
        # TODO: Handle interrupts (CTRL-C)
        self.vault.close_opened()
        database.close_connection()
        self._restore_escape_delay()
