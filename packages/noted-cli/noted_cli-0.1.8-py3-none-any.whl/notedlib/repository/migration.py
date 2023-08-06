from notedlib.database import queryone, execute

from notedlib.logging import logging

logger = logging.getLogger(__name__)


def get_schema_version():
    # Check if the table even exists
    query = """SELECT name FROM sqlite_master
        WHERE type = 'table' AND name = 'migrations'"""
    table_exists = bool(queryone(query))

    if not table_exists:
        return None

    query = "SELECT rev FROM migrations ORDER BY id DESC LIMIT 1"
    last_migration = queryone(query)
    return last_migration['rev']


def add_migration(rev, name):
    logger.debug('Adding migration: %s (%s)' % (name, rev))
    execute("INSERT INTO migrations (rev, name) VALUES (?, ?)", (rev, name))

# Migrations


def m_initial():
    execute("""
        CREATE TABLE migrations (
            id INTEGER PRIMARY KEY,
            rev INTEGER NOT NULL,
            name TEXT NOT NULL
        )""")


def m_schema():
    execute("""
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT DEFAULT NULL
        )""")
    execute("""
        CREATE TABLE tags (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )""")
    execute("""
        CREATE TABLE notes_tags (
            id INTEGER PRIMARY KEY,
            note_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        )""")
