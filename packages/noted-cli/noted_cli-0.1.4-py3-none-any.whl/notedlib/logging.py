import os
import logging
from logging.handlers import RotatingFileHandler

MAX_LOG_SIZE = 2097152  # 2MiB
BACKUP_COUNT = 7
LOG_FORMAT = '%(asctime)s,%(msecs)d {%(levelname)s} %(name)s: %(message)s'
DATE_FORMAT = '%H:%M:%S'
LOG_LEVEL = os.environ.get('LOGLEVEL', logging.WARNING)


def get_log_file():
    if os.environ.get('LOGFILE'):
        return os.environ.get('LOGFILE')

    # TODO: Log to storage, however, we have cyclic dependencies between
    # this module (logging) and storage. We also want to make sure that
    # storage directory exists
    return 'noted.log'


rfh = RotatingFileHandler(get_log_file(), maxBytes=MAX_LOG_SIZE,
                          backupCount=BACKUP_COUNT)
logging.basicConfig(format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    level=LOG_LEVEL,
                    handlers=[rfh])


logger = logging.getLogger(__name__)
logger.debug('Logging is setup')
