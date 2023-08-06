import sqlite3
from enum import Enum
from .logging import logging

logger = logging.getLogger(__name__)

connection = None


class OrderDir(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


def initialize_connection(db_file):
    """Open SQLite connection."""
    global connection
    logger.debug('Open connection')
    connection = sqlite3.connect(db_file)
    connection.row_factory = tuple_to_dict
    execute('PRAGMA foreign_keys = ON')


def tuple_to_dict(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def queryone(*args, **kwargs):
    c = connection.cursor()
    c.execute(*args, **kwargs)
    return c.fetchone()


def queryall(*args, **kwargs):
    c = connection.cursor()
    c.execute(*args, **kwargs)
    return c.fetchall()


def execute(*args, **kwargs):
    c = connection.cursor()
    c.execute(*args, **kwargs)
    connection.commit()


def close_connection():
    if connection:
        logger.debug('Close connection')
        connection.close()
