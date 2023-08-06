import os
import hashlib
from pathlib import Path
from .logging import logging
from tempfile import mkstemp

logger = logging.getLogger(__name__)


def get_directory():
    return os.path.join(str(Path.home()), '.noted')


def ensure_directory_created():
    storage_dir = get_directory()
    logger.debug('Creating storage dir if not exists %s' % storage_dir)
    Path(storage_dir).mkdir(parents=True, exist_ok=True)


def get_database_file_path():
    return os.path.join(get_directory(), 'database.db')


def shred_file(file_path, passes=3):
    logger.debug('Shredding file (with %d passes): %s' % (passes, file_path))
    with open(file_path, 'ba+') as writefile:
        length = writefile.tell()
        for i in range(passes):
            writefile.seek(0)
            writefile.write(os.urandom(length))
    os.remove(file_path)


def is_directory_empty(directory_path):
    for dirpath, dirnames, files in os.walk(directory_path):
        return not files

    return True


def get_file_extension(file_path):
    extensions = get_file_extensions(file_path)
    return extensions[-1] if extensions else ''


def get_file_extensions(file_path):
    return Path(file_path).suffixes


def get_file_checksum(file_path):
    md5hash = hashlib.md5()

    with open(file_path, 'rb') as readstream:
        for chunk in iter(lambda: readstream.read(4096), b''):
            md5hash.update(chunk)
    return md5hash.hexdigest()


def directory_exists():
    return os.path.exists(get_directory())


def is_empty():
    return is_directory_empty(get_directory())


def create_temp_file(filename):
    tmppath = mkstemp(suffix='_' + filename)
    return tmppath[1]
