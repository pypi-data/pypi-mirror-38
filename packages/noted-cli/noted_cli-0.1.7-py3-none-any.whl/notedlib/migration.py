from notedlib.logging import logging
import notedlib.repository.migration as migration_repo

logger = logging.getLogger(__name__)

# NOTE: do not remove or change order of these, append only
migrations = [
    'm_initial',
    'm_schema',
]


def migrate():
    """Executes migrations to database schema if needed."""
    logger.debug('Checking if migration is needed')
    current_schema_version = migration_repo.get_schema_version()

    if current_schema_version is None:
        logger.debug('Initial migration has not been done')
        migration_start = 0
    else:
        migration_start = current_schema_version + 1

    # TODO: backup database before running any migrations
    rev = 0

    for rev in range(migration_start, len(migrations)):
        logger.info('Running migration: %s since current version was: %s' % (
            migrations[rev], current_schema_version))
        getattr(migration_repo, migrations[rev])()
        migration_repo.add_migration(rev, migrations[rev])
